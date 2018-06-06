def main():
    filename=input("Enter the file name(with '.txt' extension): ")
    if filename == "imdb.txt":
        outfile=open("imdb.csv",'w')
    elif filename == "nytimeshealth.txt":
        outfile=open("nytimeshealth.csv",'w')

    documents = create_documents(filename)

    itrf={}
    matrix=[]
    temp=['TF-IDF']

    for document_key,document_contents in documents.items():
        for term in set(documents[document_key]):
            tf=term_frequency(term,documents[document_key])
            itf=inverse_document_frequency(term,documents)
            trf_idf=round((tf*itf),2)
            itrf[term]=trf_idf

    import operator as operator
    sorted_itrf = dict(sorted(itrf.items(), key=operator.itemgetter(1),reverse=True))
    for word in sorted_itrf:
        temp.append(word)
    matrix.append(temp)
    head=matrix[0]
    head=",".join(head)
    outfile.write(head+'\n')
    Matrix = [[0 for x in range(len(matrix[0]))] for y in range(len(documents))]
    out=[]
    for document_key,document_contents in documents.items():
        out.append("d{}".format(document_key+1))
        for term in sorted_itrf:
            tf=term_frequency(term,documents[document_key])
            itf=inverse_document_frequency(term,documents)
            trf_idf=round((tf*itf),2)
            out.append(str(trf_idf))

        out=",".join(out)
        outfile.write(out+'\n')
        out=[]
    print("Complete..... Thank you for your patience.")


def create_documents(filename):

    documents={}
    documents_file = open(filename, encoding="utf8")
    line=documents_file.readline()

    i=0
    while line !="":
        document_key=i
        document_contents=line
        document_contents=clean_document_contents(document_contents,filename)
        documents[document_key]=document_contents
        line=documents_file.readline()
        i+=1
    return documents


def clean_document_contents(document_content,filename):

    import re
    if filename == "nytimeshealth.txt":
        document_content = document_content.split("|")
        document_content = str(document_content[2])
    document_content= re.sub(r"http\S+", "", document_content)
    document_content=document_content.lower()
    document_content=re.sub('[^a-z]',' ' ,document_content)
    document_content=document_content.strip()
    document_content_list_temp=document_content.split(" ")
    document_content_list=[]

    for item in document_content_list_temp:
        if item!="":
            document_content_list.append(item)

    return document_content_list


def term_frequency(term,document_content):
    term_frq={}
    termdict=dict((document_content[n],0 )for n in range(len(document_content)))

    for key in document_content:
        termdict[key]+=1


    length=len(document_content)
    if length==0:
        divisor=1
    else:
        divisor=length
    trf=termdict.get(term,0)/divisor

    return trf


def inverse_document_frequency(term, documents):
    import math as math
    count=0
    for document_key in documents:
        if term in documents[document_key]:
            count=count+1

    idf=math.log10((len(documents))/count)

    return idf

main()
