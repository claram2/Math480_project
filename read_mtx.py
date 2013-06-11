import urllib
import tarfile
import shutil
import os
import gzip

from sage.graphs.graph import Graph
from sage.graphs import graph

def Read_mtx(graph_string):
    """
    This function takes in either the url of a graph in Matrix Market format or the path to a Matrix Market file and
    reads it in to create a sage graph. If reading in a file on from the file system it must be in Matrix Market format.
    If a url is given it must end in .mtx.gz or in .tar.gz form.
    Two recomended sites for finding Matrix Market format graphs are:
        http://www.cise.ufl.edu/research/sparse/matrices/index.html
        http://math.nist.gov/MatrixMarket/

    EXAMPLE::
    sage: g_1=graphs.Read_mtx('http://www.cise.ufl.edu/research/sparse/MM/Bates/Chem97Zt.tar.gz')
    sage:
    sage: g_2=graphs.Read_mtx('ftp://math.nist.gov/pub/MatrixMarket2/Harwell-Boeing/bcsstruc1/bcsstk01.mtx.gz')
    sage:
    sage: g_3=graphs.Read_mtx('./impcol_a.mtx')

    REFERENCES:
    Matrix Market format: http://math.nist.gov/MatrixMarket/formats.html#MMformat
    """
    parsing = graph_string.split('/')
    if not (parsing[0] == 'http:' or parsing[0] == 'ftp:'):
        return read_mtx_file(graph_string)
    else:
        extensions = parsing[len(parsing)-1].split('.')
        if extensions[len(extensions)-2] == 'tar':
           return read_mtx_url_tar(graph_string, extensions[0])
        else:
           return read_mtx_url_gz(graph_string, extensions[0])

def read_mtx_url_tar(url, filename):
    urllib.urlretrieve(url, "temp.tar.gz")
    tfile = tarfile.open("temp.tar.gz", 'r:gz')
    tfile.extractall('.')
    from sage.graphs.all import Graph
    g = read_mtx_file(filename + '/' + filename + '.mtx')
    shutil.rmtree(filename)
    os.remove('temp.tar.gz')
    return g

def read_mtx_url_gz(url, filename):
    urllib.urlretrieve(url,'temp.mtx.gz')
    f = gzip.open('temp.mtx.gz', 'rb')
    g = read_mtx(f)
    g.name(filename)
    os.remove('temp.mtx.gz')
    return g

def read_mtx_file(filename):
    from sage.graphs.all import Graph
    f = open(filename)
    g = read_mtx(f)
    g.name(filename)
    return g

def read_mtx(f):
    contents = f.readlines()
    edges = []
    first = 0
    for i in range(len(contents)):
        words = contents[i].split()
        if words[0][0] != '%':
            if first == 0:
                first = 1
            else:
                if(len(words) == 3):
                    edges.append((int(words[0]), int(words[1]), float(words[2])))
                else:
                    edges.append((int(words[0]), int(words[1]), None))

    g = Graph()
    g.add_edges(edges)
    return g

