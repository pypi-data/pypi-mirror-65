#!/usr/bin/env python3
#!/usr/bin/env python2

"""
Groups together a few utilities to manage the knngraph and metadata of F100M
"""

import sys
import subprocess

import pdb
import random
import os
import urllib
import _pickle as cPickle
import pickle
import numpy as np
import codecs


from multiprocessing.dummy import Pool as ThreadPool



"""
cp /mnt/vol/gfsai-east/ai-group/datasets/flickr100m_graph/{id_to_flickr.long3,flickr_to_id.long2,geoloc.double3,times.long4,urls.long3} /data/users/matthijs/f100m/metadata_cache

cp /mnt/vol/gfsai-east/ai-group/datasets/flickr100m_graph/{line_to_flickr.long2,flickr_to_line.long2} /data/users/matthijs/f100m/metadata_cache/

cp XXX/yfcc100m_dataset.bz2 /data/users/matthijs/f100m/metadata_cache/
bunzip2 yfcc100m_dataset.bz2
"""


f100m_basedir = '/scratch/matthijs/flickr100m/'

if not os.path.exists(f100m_basedir):
    f100m_basedir = '/checkpoint/matthijs/flickr100m/'

f100m_metadatadir = "/datasets01/yfcc100m/090517/"



def mmap_neighbor_tables(dataset, do_load=False):
    f100m_graph_dir = f100m_basedir + '/flickr100m_graph/'
    k = 100

    if dataset == "1Mrmac":
        filename_I = f100m_graph_dir + '/I_1Mrmac.raw'
        filename_D = f100m_graph_dir + '/D_1Mrmac.raw'
    elif dataset in ('100Mrmac_nn15', '95Mresnet_nn15', '100Mtoplevel_nn15'):
        filename_I = f100m_graph_dir + 'I_%s.raw' % dataset
        filename_D = f100m_graph_dir + 'D_%s.raw' % dataset
        k = 15
    else:
        assert False

    if not do_load:
        I = np.memmap(filename_I, dtype='int32', mode='r').reshape(-1, k)
        D = np.memmap(filename_D, dtype='float32', mode='r').reshape(-1, k)
    else:
        I = np.fromfile(filename_I, dtype='int32').reshape(-1, k)
        D = np.fromfile(filename_D, dtype='float32').reshape(-1, k)

    assert D.shape == I.shape

    return D, I




# the 1st column of tab contains the flickr imno that the line is referring to
# bissects to find the fimno. If not found, returns None
def find_fimno_in_table(tab, flickrno):
    i0, i1 = 0, tab.shape[0]
    while i0 + 1 < i1:
        imed = (i1 + i0) / 2
        if tab[imed, 0] <= flickrno:
            i0 = imed
        else:
            i1 = imed
    if tab[i0, 0] == flickrno:
        return i0
    else:
        return None


# interpolation search. Not useful in this case because the mapping is concave
def find_fimno_in_table_2(tab, flickrno):
    n = tab.shape[0]
    i0, i1 = 0, n - 1
    f0 = tab[i0, 0]
    f1 = tab[i1, 0]
    if flickrno > f1 or flickrno < f0: return None
    if flickrno == f1: return i1
    if flickrno == f0: return 0
    while i0 + 1 < i1:
        frac = (flickrno - f0) / float(f1 - f0)
        print(flickrno, (i0,  f0), (i1 - i0, f1 - f0), frac, i1 - i0, f1 - f0)
        imed = i0 + 1 + (i1 - i0 - 1) * (flickrno - f0) / (f1 - f0)
        fmed = tab[imed, 0]
        print("  ", imed, fmed, fmed <= flickrno)
        if fmed == flickrno:
            return imed
        elif fmed < flickrno:
            i0 = imed
            f0 = fmed
        else:
            i1 = imed
            f1 = fmed
    if tab[i0, 0] == flickrno:
        return i0
    else:
        return None



class F100MIDMapper2:
    """To be used with the main metadata file that uses line numbers as keys. """

    def __init__(self, name_map_fname, inv_name_map_fname, force_preload=False):
        if force_preload:
            name_map = np.fromfile(name_map_fname, dtype=int)
            inv_name_map = np.fromfile(inv_name_map_fname, dtype=int)
        else:
            name_map = np.memmap(name_map_fname, dtype=int, mode='r')
            inv_name_map = np.memmap(inv_name_map_fname, dtype=int, mode='r')

        self.name_map = name_map.reshape(-1, 2)
        self.inv_name_map = inv_name_map.reshape(-1, 2)
        self.n = self.name_map.shape[0]
        assert self.n == self.inv_name_map.shape[0]
        metadata_fname = f100m_metadatadir + 'yfcc100m_dataset.txt'
        self.metadata = np.memmap(metadata_fname, dtype='uint8', mode='r')

    def imno_to_flickr(self, imno):
        return self.name_map[imno][0]

    def flickr_to_imno(self, flickrno):
        i = find_fimno_in_table(self.inv_name_map, flickrno)
        if i is None:
            return None
        else:
            return self.inv_name_map[i, 1]

    def imno_to_metadata(self, imno):
        i0 = self.name_map[imno, 1]
        if imno + 1 < self.name_map.shape[0]:
            i1 = self.name_map[imno + 1, 1]
        else:
            i1 = self.metadata.size
        return self.metadata[i0:i1].tostring()

    def flickr_to_description(self, fimno):
        imno = self.flickr_to_imno(fimno)
        if not imno: return None
        l = self.imno_to_metadata(imno)
        return urllib.unquote_plus(l.split('\t')[9])

    def flickr_to_words(self, fimno):
        imno = self.flickr_to_imno(fimno)
        if not imno: return None
        l = self.imno_to_metadata(imno)
        tags = ''
        for fi in l.split('\t')[8:11]:
            if not fi: continue
            utf8_string = urllib.unquote_plus(fi)
            unicode_s = unicode(utf8_string, 'utf-8')
            unicode_s = unicode_s.replace('<', '&lt')
            unicode_s = unicode_s.replace('>', '&gt')
            tags += ' ' + unicode_s
        return tags.encode('UTF-8')

    def imno_to_tags_unicode(self, imno):
        l = self.imno_to_metadata(imno)
        tags = ''
        for fi in l.split('\t')[8:11]:
            if not fi: continue
            utf8_string = urllib.unquote_plus(fi)
            unicode_s = unicode(utf8_string, 'utf-8')
            tags += ' ' + unicode_s
        return tags

    def flickr_to_filename(self, fimno):
        return "%d" % fimno

def get_metadata():
    return  F100MIDMapper2(
        f100m_basedir + 'metadata/line_to_flickr.long2',
        f100m_basedir + 'metadata/flickr_to_line.long2')



class Geoloc:
    " geolocalization info "
    def __init__(self):
        geoloc = np.fromfile(f100m_dir + 'geoloc.double3', dtype='float64')
        self.geoloc = geoloc.reshape(-1, 3)

    def get_geoloc(self, imno):
        """ takes a Flickr id as input"""
        i = find_fimno_in_table(self.geoloc, imno)
        return self.geoloc[i, 1:] if i is not None else None

class Dates:
    "date+time information"
    def __init__(self):
        dates = np.fromfile(f100m_dir + 'times.long4', dtype='uint64')
        self.dates = dates.reshape(-1, 4)
        self.datesc = self.dates.view('uint8')

    def date_in_s(self, fimno):
        i = find_fimno_in_table(self.dates, fimno)
        if i is None: return
        return self.dates[i, 1]

    def date_string(self, fimno):
        i = find_fimno_in_table(self.dates, fimno)
        if i is None: return
        return self.datesc[i, 16:16+15].tostring()

    def date_s_and_string(self, fimno):
        i = find_fimno_in_table(self.dates, fimno)
        if i is None: return None, None
        return self.dates[i, 1], self.datesc[i, 16:16+15].tostring()

class Urls:

    def __init__(self):
        urls = np.fromfile(f100m_dir + 'urls.long3', dtype='uint64')
        self.urls = urls.reshape(-1, 3)

    def get_flickr_url(self, fimno):
        i = find_fimno_in_table(self.urls, fimno)
        if i is None: return
        t = self.urls[i, 1:]
        t0, t1 = int(t[0]), int(t[1])
        return "http://farm%d.staticflickr.com/%d/%d_%x.jpg" % (
            t0 >> 56, (t0 >> 40) & 0xffff, t0 & 0xffffffffff, t1)


class EverstoreUrls():

    def __init__(self):
        self.tab = np.memmap(
            f100m_metadatadir + '/images/everstore_urls.dat',
            mode='r', dtype = 'uint8').reshape(-1, 112)

    def get_url(self, lineno):
        return self.tab[lineno].tostring().strip()



class F100MrmacDescriptors:

    def __init__(self):
        self.bs = 200000
        self.basedir = '/mnt/vol/gfsai-east/ai-group/users/matthijs/compute_f100m_rmac'
        self.thread_pool = ThreadPool(40)

    def load_descriptors(self, indices):

        def load_1(i):
            bno = i / self.bs
            fname = "%s/features_%d:%d.npy" % (
                self.basedir, bno * self.bs, (bno + 1) * self.bs)
            x = np.load(fname, mmap_mode='r')
            return x[i - bno * self.bs]

        res = np.vstack(self.thread_pool.map(load_1, indices))
        res /= np.sqrt((res ** 2).sum(1)).reshape(-1, 1)
        return res


class DocWordMatrix:
    """returned image numbers must be translated with F100MIDMapper2 """

    def __init__(self,
                 dataset='100M',
                 voc='freq200k_bad200',
                 load_cooc=False):

        basedir = f100m_basedir + "doc_word_matrix/"
        self.fromwhere = (basedir, dataset, voc)

        reduced_word_list_fname = basedir + "/tags_%s_voc_%s_word_list.pickle" % (
            dataset, voc)

        matrixT_fname = dict([(field, basedir + "tags_%s_voc_%s_matrixT_%s.npy" % (
            dataset, voc, field)) for field in ['data', 'indices', 'indptr']])
        
        with open(reduced_word_list_fname, "rb") as fdata:
            read = fdata.read()
            self.word_list = pickle.loads(read)
#         self.word_list = cPickle.load(open(reduced_word_list_fname, 'rb').read().encode('utf-8').strip())
        self.sorted_word_list = self.word_list[:]
        self.sorted_word_list.sort()

        self.word_to_id = dict([(word, i) for i, word in enumerate(self.word_list)])

        # do not build the CSR structure to avoid loading the mmapped
        # data if not used.
        self.matrixT = {}
        for field in matrixT_fname:
            self.matrixT[field] = np.load(matrixT_fname[field], mmap_mode='r')

        if not load_cooc: return

        cooc_voc_fname = dict([(field, basedir + "tags_%s_voc_%s_cooc_%s.npy" % (
            dataset, voc, field)) for field in ['data', 'indices', 'indptr']])

        # same
        self.cooc = {}
        for field in matrixT_fname:
            self.cooc[field] = np.load(cooc_voc_fname[field], mmap_mode='r')


    def word_to_imnos(self, word):
        wi = self.word_to_id[word]
        indptr = self.matrixT['indptr']
        i0, i1 = indptr[wi], indptr[wi + 1]
        imnos = self.matrixT['indices'][i0:i1]
        return imnos

    def cooc_words(self, word, min_cooc=100):
        wi = self.word_to_id[word]
        indptr = self.cooc['indptr']
        i0, i1 = indptr[wi], indptr[wi + 1]
        wi2s = self.cooc['indices'][i0:i1]
        nocc = self.cooc['data'][i0:i1]
        wi2s = wi2s[nocc >= min_cooc]
        return [self.word_list[wi2] for wi2 in wi2s]

    def load_direct_matrix(self):
        (basedir, dataset, voc) = self.fromwhere

        matrix_fname = dict([(field, basedir + "tags_%s_voc_%s_matrix_%s.npy" % (
            dataset, voc, field)) for field in ['data', 'indices', 'indptr']])

        # do not build the CSR structure to avoid loading the mmapped
        # data if not used.
        self.matrix = {}
        for field in matrix_fname:
            self.matrix[field] = np.load(matrix_fname[field], mmap_mode='r')
            
#################################################
# some text related functions

excluded_tags = set(['NULL', 'www', 'img', 'jpg', 'href', 'dsc',
                     'the', 'in', 'of', 'to', 'on', 'from', 'and',
                     'www', 'nofollow', 'com', 'del', 'net', 'que',
                     'rel', 'http', 'you', 'lta', 'sca'])


translation_only_alphanum = ''.join([
    (chr(i) if ('a' <= chr(i) <= 'z' or
                '0' <= chr(i) <= '9' or
                'A' <= chr(i) <= 'Z') else ' ') for i in range(256)])

def tokenizer(tagl):
    # convert to ascii, dropping any non-ascii characters
    tagl = unicode(tagl, 'utf-8')
    tagl = tagl.encode('ascii', 'replace')
    # also drop non-alphanumerics
    tagl = tagl.translate(translation_only_alphanum)
    return tagl.lower().split()

def tag_BoW_robust(tagl):

    tagl = tokenizer(' '.join(tagl))

    hist = {}
    for w in tagl:
        if len(w) < 3: continue
        if w in excluded_tags: continue

        if w in hist:
            hist[w] += 1
        else:
            hist[w] = 1
    sorted_dict = [(nocc, w) for w, nocc in hist.items()]
    sorted_dict.sort()
    sorted_dict.reverse()
    return sorted_dict



if __name__ == '__main__':

    D, I = mmap_neighbor_tables('100Mrmac_nn15')

    print(D.shape)

    docw = DocWordMatrix(load_cooc=False)
    
    print(docw.word_to_imnos('trein'))

    metadata = get_metadata()

    print(metadata.imno_to_metadata(123456))
