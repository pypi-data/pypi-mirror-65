#! /usr/bin/python
# -*- coding: utf-8 -*-
from foqus.commons import download
from foqus.customers import *
from foqus.pipline_cutomise import *
from foqus.request_api import APIFoqus
from foqus.server_apis import classfication_after_similars
from six.moves import http_client

from urllib.parse import urlparse
from urllib.request import urlopen

import imghdr
import mimetypes
import tensorflow as tf
import requests
import shutil
import xlrd

api = APIFoqus()


def load_labels(label_file):
    if '://' in label_file:
        response = urlopen(label_file)
        proto_as_ascii_lines = response.read()
        label = proto_as_ascii_lines.decode('utf-8').split('\n')
    else:
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
    return label


def count_images_folders(path):
    x = 0
    for i in os.listdir(str(path)):
        x = x + 1
    return x


def load_graph(model_file):
    if '//' in model_file:
        try:

            logger.info('Getting graph from %s' %model_file)
            response = urlopen(model_file).getcode()
            if response == 200:
                graph = tf.Graph()
                graph_def = tf.GraphDef()
                file = urlopen(model_file)
                file_content = file.read()
                graph_def.ParseFromString(file_content)
                with graph.as_default():
                    tf.import_graph_def(graph_def)
                return graph
            else:
                logger.info('file %s Not exisiting in server' %model_file)

        except Exception as e:
            logger.error('Error %s in getting graph from remote server %s'% (e, model_file))
    else:
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)
        return graph
    return None


def load_json_data(json_path):
    try:
        with open(json_path) as data_file:
            json_input = json.load(data_file)
    except:
        json_data = open(json_path)
        bom_maybe = json_data.read(3)
        if bom_maybe != codecs.BOM_UTF8:
            json_data.seek(0)
        json_input = json.load(json_data)
    return json_input


def checkUrl(url):
    p = urlparse(url)
    conn = http_client.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400


def is_url_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg", "binary/octet-stream")
    r = requests.head(image_url)
    if r.headers["content-type"] not in image_formats:
        mimetype, encoding = mimetypes.guess_type(image_url)
        return mimetype and mimetype.startswith('image')
    else:
        return True


def image_extension(image_url):
    r = requests.head(image_url)
    if r.headers["content-type"]:
        return r.headers["content-type"].split('/')[1]
    else:
        return image_url.split('.')[-1]



def max_nb_images(path):
    list_nbrs = []
    for j in os.listdir(path):
        for k in os.listdir(str(path) + "/" + str(j)):
            ext = imghdr.what(str(path) + "/" + str(j) + "/" + str(k))
            if (ext == 'png' and k.split(".")[1] in ['jpg', 'jpeg', 'JPG', 'JPEG']) or \
                    (ext in ['jpeg', 'jpg'] and k.split('.')[1] in ['png', 'PNG']) or (ext is None):
                os.remove(str(path) + "/" + str(j) + "/" + str(k))
                logger.info("Deleting_image as it contains png encoding - " + str(path) + "/" + str(j) + "/" + str(k))
        list_nbrs.append(len(os.listdir(str(path) + "/" + str(j))))
    return max(list_nbrs)


def verif_folder_less_twenty(path):
    image_ext = ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']
    folder_less_20 = []
    max_nb = max_nb_images(path)
    if max_nb < 20:
        max_nb = 20
    for j in os.listdir(path):
        x = 0
        for i in os.listdir(str(path) + "/" + str(j)):
            if os.path.splitext(i)[1] in image_ext:
                x = x + 1
        if x == 0 :
            shutil.rmtree(str(path) + "/" + str(j))
            logger.info("Deletin Empty folder : " + str(path) + "/" + str(j))
        elif (x <= 20 or x < max_nb):
            logger.info("WARNING: Folder has less images : " + str(j).split('/')[-1])
            folder_less_20.append(str(j).split('/')[-1])
    return folder_less_20, max_nb


def generate_more_images(training_path, folders, max_nb):
    for id_categorie in folders:
        DIR = str(training_path) + "/" + str(id_categorie)
        nb_images = (len(os.listdir(DIR)))
        p = Pipeline2(source_directory=DIR, output_directory=DIR)
        p.rotate(probability=1, max_left_rotation=5, max_right_rotation=5)
        p.flip_left_right(probability=0.5)
        p.zoom_random(probability=0.5, percentage_area=0.8)
        p.flip_top_bottom(probability=0.5)
        p.sample(max_nb - nb_images)
    logger.info("The images increase is done successfully")


def read_tensor_from_image_file(file_name, input_height=299, input_width=299, input_mean=0, input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(file_reader, channels = 3,
                                           name='png_reader')
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                      name='gif_reader'))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
    else:
        image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                            name='jpeg_reader')
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)
    return result


def fill_prediction_table(path_file_Final, customer_type, customer_name, customer_universe):
    table_name = "predict_" + customer_type + '_' + customer_name + '_' + customer_universe
    db.create_prediction_table(table_name)
    workbook = xlrd.open_workbook(path_file_Final)
    sheet = workbook.sheet_by_name(workbook.sheet_names()[0])
    nRows = sheet.nrows

    db.delete_predict_table(table_name)
    for i in range(1, nRows):
        row_values = sheet.row_values(i)
        if row_values[12] != "":
            principal_categorie = str((row_values[12]))
        else:
            if row_values[10] != "":
                principal_categorie = str((row_values[10]))
            else:
                principal_categorie = str((row_values[8]))
        db.add_prediction_table(table_name, row_values, principal_categorie)


def process_customer_stream_from_json(json_path, customer_name, customer_type, project_name):
    request_post = api.apipost('retrieve_images_json', customer_name, customer_type, project_name, json_path)
    response_text = json.loads(request_post.text)
    response = response_text['response']
    response = 1
    if int(response) != 0:
        if generate_similarity_vector(customer_name, customer_type, project_name):
            user_apikey = db.get_apikey_from_customer(customer_name)[0]
            classfication_after_similars(user_apikey, customer_name, customer_type, project_name)


def process_customer_stream_cms(json_path, customer_name, customer_type, project_name):
    streams_path = STREAMS_PATH + customer_type + '/' + customer_name + '/similars/' + project_name + '/'+ \
                   'cms_json_file.json'
    streams_paths3 = STREAMS_S3 + customer_type + '/' + customer_name + '/similars/' + project_name + '/'
    if '://' in json_path:
        download(json_path, streams_path)
    else:
        streams_path = json_path
    upload_file_into_s3(streams_path, streams_paths3)
    # TODO appel fonction process customer from stream après traitement de fichier json des produits
    # process_customer_stream_from_json(json_path, customer_name, customer_type,project_name)


def get_redirect_url(url):
    try:
        image = requests.get(url)
        if image.url == url:
            return is_url_image(url)
        else:
            return is_url_image(image.url)
    except:
        return False


def detection_error_training(excel_path, customer_name, customer_type, customer_universe):
    api.apipost('training_text_detection', customer_name, customer_type, None, excel_path, customer_universe)


def equilibrate_customer_samples_count(excel_path, customer_name, customer_type, customer_universe):
    api.apipost('correction_training', customer_name, customer_type, None, excel_path, customer_universe)


def shopify_training(customer_name, customer_type, url_shop, project, INPUT_SESSION_UUID):
    api.apipost('shopify_training', customer_name, customer_type, None, None, project, url_shop, INPUT_SESSION_UUID)


def generate_similarity_vector(customer_name="vector", customer_type='vector', project_name=None):
    vector_response = api.apipost('training_similars', customer_name, customer_type, project_name, None, None)
    response_text = json.loads(vector_response.text)
    response_from_parquet = response_text['response']
    if response_from_parquet == 2:
        return True
    return False


def text_training_retrieve_json(excel_path, customer_name, customer_type, customer_universe, project_name):
    send_email_when_training_started(customer_name, project_name, 'classification', 'Training started')
    if project_name:
        operation = 'training_classification'
    else:
        operation = 'training_text_detection'

    api.apipost(operation, customer_name, customer_type, project_name, excel_path, customer_universe)


def classification_similars(customer_name, customer_type, project_name):
    api.apipost("classification_similars", customer_name, customer_type, project_name)

