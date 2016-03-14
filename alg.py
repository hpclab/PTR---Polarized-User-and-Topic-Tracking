# to run it
#python algPTR.py arg1 arg2 arg3
# db=twitter
# collection=refugees
#arg1 db, arg2 collection, arg3 nome file tweet, arg4  time or not (1,0), arg5 num iterations or num days , arg6 file con i seed, arg 7 param

def clean_collection(collection):
    #print "Cleaning..."
    collection.update({}, {'$unset': {"us_final":1}}, multi=True)
    collection.update({}, {'$unset': {"tw_pr":1}}, multi=True)

def mostcommon(iterable, n=None):
    """Return a sorted list of the most common to least common elements and
    their counts.  If n is specified, return only the n most common elements.

    """
    #import operator
    bag = {}
    bag_get = bag.get
    for elem in iterable:
        bag[elem] = bag_get(elem, 0) + 1
    if n is None:
        return sorted(bag.iteritems(), key=itemgetter(1), reverse=True)
    it = enumerate(bag.iteritems())
    nl = nlargest(n, ((cnt, i, elem) for (i, (elem, cnt)) in it))
    return [(elem, cnt) for cnt, i, elem in nl]

def get_data(file_class):
    final_dic={}
    rawfile=open(file_class, 'r')
    with rawfile as f:
        cnt=0
        for line in f:
            cnt+=1
            if line[-1]=='\n':
                line=line[:-1]
            line=line.split(' ')
            exec("class"+str(cnt)+"=[]")
            for i in line:
                exec("class"+str(cnt)+".append(i.lower())")
            final_dic["class"+str(cnt)]=eval("class"+str(cnt))

    return final_dic


def polarization_track(collection, iteration, param, **final_dic):
    partiti=final_dic.keys()
    num_partiti=len(partiti)
    clean_collection(collection)
    #udic=[]
    #hdic=[]
    out=[]
    out.append("")
    print ("")
    out.append("Iterative procedure: " + str(iteration)+ " iterations.")
    print ("Iterative procedure: " + str(iteration)+ " iterations.")
    out.append("total tweets: "  + str(collection.find().count()))
    print ("total tweets: "  + str(collection.find().count()))
    out.append("total users: "  + str(len(collection.find().distinct("user"))))
    print ("total users: "  + str(len(collection.find().distinct("user"))))
    print ""
    #cic numero di iterazioni
    for cic in range(int(iteration)):
        out.append(datetime.now().time())
        print (datetime.now().time())
        out.append('STEP '+ str(cic+1))
        print ('STEP '+ str(cic+1))
        print ""
        out.append("tweets classification")
        print ("tweets classification")
        #logging.info('Step: '+str(cic))
        us_tw_dic={}
        for tweet in collection.find():
            conto_p=0
            for part in partiti:
                if conto_p>1:
                    break
                for i in tweet[u'ht']:
                    if i in final_dic[part]:
                        conto_p+=1
                        part_name=part
                        break
            if conto_p==1:
                collection.update({"_id":tweet['_id']},{'$set': {"tw_pr": part_name}})
                if us_tw_dic.has_key(int(tweet[u'user'])):
                    us_tw_dic[int(tweet[u'user'])].append(partiti.index(part_name))
                else:
                    us_tw_dic[int(tweet[u'user'])]=[partiti.index(part_name)]

        out.append("classified tweets:")
        print ("classified tweets:")
        out.append(collection.find({"tw_pr":{'$exists': True}}).count())
        print (collection.find({"tw_pr":{'$exists': True}}).count())
        #logging.info('tw '+str(collection.find({"tw_pr":{'$exists': True}}).count()))
        out.append(datetime.now().time())
        print (datetime.now().time())
        print ""


        #user_id=collection.find({"tw_pr":{'$exists': True}}).distinct("user")

        out.append("users classification")
        print ("users classification")

        us_dic={}

        pnt=0
        for i in us_tw_dic.keys():
            pnt+=1
            #if pnt%100000==0:
            #    print pnt
            list_part=us_tw_dic[i]
            most_list=mostcommon(list_part)
            if len(most_list)==1 or most_list[0][1]>(most_list[1][1])*2:
                us_dic[i]=most_list[0][0]

        #udic.append(us_dic)

        out.append("classified users:")
        print ("classified users:")
        out.append(len(us_dic.keys()))
        print (len(us_dic.keys()))
        out.append(datetime.now().time())
        print (datetime.now().time())
    #    print len(collection.find({"us_final":{'$exists': True}}).distinct("user"))
        #logging.info('us '+str(len(us_dic)))
        #print datetime.now().time()


        #H_list=[]
        #Edges=[]
        hash_score={}
        #param=0.002
        part_ht=[]
        part_ht_dict=[]
        out.append("")
        print ("")

        for part in partiti:
            out.append(part)
            print (part)
            #print "graph construction"
            hashtag={}
            num_tot_tw=0
            for a in collection.find():
                if us_dic.has_key(int(a[u'user'])):
                    if us_dic[int(a[u'user'])]==partiti.index(part):
                        num_tot_tw+=1
                        parole=[]
                        for i in a[u'ht']:
                            parole.append(i)
                        for p in set(parole):
                            if hashtag.has_key(p.lower()):
                                hashtag[p.lower()]+=1
                            else:
                                hashtag[p.lower()]=1

    #         for q in polar_h:
    #             if hashtag.has_key(q):
    #                 del hashtag[q]

            list_hashtag=[(k,v) for v,k in sorted([(v,k) for k,v in hashtag.items()],reverse=True) if v>1]
            #hot_hashtag=[]
            list_hash=[]
            for i in list_hashtag:
                #hot_hashtag.append(i[0])
                list_hash.append(i[0])


            out.append('retrieved hashtags')
            print ('retrieved hashtags')

            #H=nx.Graph()
            #for i in mostcommon(edges):
                #H.add_edge(i[0][0], i[0][1],weight=i[1]/float(mostcommon(edges)[0][1]))
            #H_list.append(H)

            #exec("%s_upd=list_hash" % part) in globals(), locals()
            #print part
            out.append(len(list_hash))
            print (len(list_hash))
            out.append(datetime.now().time())
            print (datetime.now().time())


            for h in list_hash:
                if hashtag.has_key(h):
                    score=hashtag[h]/float(num_tot_tw)
                else:
                    score=0
    #             if h in eval(part):
    #                 score=1
    #             else:

    #                 calc2=0
    #                 for a in collection.find({"us_final2": part}):
    #                     if h in a[u'ht']:
    #                         if len(set(a[u'ht']).intersection(eval(part)))>0:
    #                             calc2+=1

    #                 val=calc2
    #                 score=round(val/float(hashtag[h] + calc1 - val),5)

                if hash_score.has_key(h):
                    hash_score[h][partiti.index(part)]=score

                else:
                    hash_score[h]=[]
                    for np in range(len(partiti)):
                        hash_score[h].append(0)

                    hash_score[h][partiti.index(part)]=score
            #exec("%s=[]" % part)
            #exec("%sdic={}" % part)
            final_dic[part]=[]
            #part_ht.append([])
            part_ht_dict.append({})

        #out.append(datetime.now().time())

        for k,v in hash_score.iteritems():
            max_h=max(v)
            cnt=v.index(max_h)
            v=filter(lambda a: a != max_h, v)
            if len(v)==(len(partiti)-1):
                kval=1
                for val_v in v:
                    kval=kval*(1-float(val_v))
                fscore=round(max_h*(kval),5)
                if fscore>param:
                    #print k
                    #print max_h
                    part=partiti[cnt]
                    #exec("%s.append(k)" % part)
                    #exec("%sdic[k]=fscore" % part)
                    final_dic[part].append(k)
                    part_ht_dict[partiti.index(part)][k]=fscore
        #print datetime.now().time()
        #for part in partiti:
        #    hdic.append(eval(part))

        for part in partiti:
            out.append('\n')
            print ('\n')
            out.append('TOPICS:')
            print ('TOPICS:')
            out.append(part)
            print (part)
            out.append(len(final_dic[part]))
            print (len(final_dic[part]))
            out.append([(k,v) for v,k in sorted([(v,k) for k,v in part_ht_dict[partiti.index(part)].items()],reverse=True)])
            print ([(k,v) for v,k in sorted([(v,k) for k,v in part_ht_dict[partiti.index(part)].items()],reverse=True)])


        #print collection.find().count()
        for part in partiti:
            print ('\n')
            out.append(part)
            print (part)
            out.append('polarized tweets: ' + str(collection.find({"tw_pr": part}).count()))
            print ('polarized tweets: ' + str(collection.find({"tw_pr": part}).count()))
            n2=len([i for i in us_dic.values() if i==partiti.index(part)])
            out.append('polarized users: ' + str(n2))
            print ('polarized users: ' + str(n2))
        out.append('\n')
        print ('\n')
        out.append('total polarized users: ' + str(len(us_dic)))
        print ('total polarized users: ' + str(len(us_dic)))
        out.append('\n')
        print ('\n')


        collection.update({}, {'$unset': {"tw_pr":1}}, multi=True)
    return out

def time_polarization_track(collection, ndays, param, **final_dic):
    partiti=final_dic.keys()
    num_partiti=len(partiti)
    clean_collection(collection)

    #udic=[]
    #hdic=[]
    #cic numero di iterazioni



    us_dic={}
    dlist=collection.find().distinct("day")
    dlist.sort()
    out=[]
    out.append("")
    print ("")
    out.append("Procedure with time iteration: every " + str(ndays)+ " days.")
    print ("Procedure with time iteration: every " + str(ndays)+ " days.")
    out.append("total tweets: "  + str(collection.find().count()))
    print ("total tweets: "  + str(collection.find().count()))
    out.append("total users: "  + str(len(collection.find().distinct("user"))))
    print ("total users: "  + str(len(collection.find().distinct("user"))))
    print ("")

    for cic in range(int(nup.ceil(len(dlist)/ndays))):
        out.append(datetime.now().time())
        print (datetime.now().time())
        out.append('step '+ str(cic+1))
        print ('STEP '+ str(cic+1))
        print ("")
        out.append("tweets classification")
        print ("tweets classification")
        us_tw_dic={}

        if ((cic+1)*ndays)>len(dlist)-1:
            end_d=dlist[len(dlist)-1]+1
        else:
            end_d=dlist[(cic+1)*ndays]

        for tweet in collection.find({"day": { "$gt": dlist[cic*ndays]-1, "$lt": end_d}}):
            conto_p=0
            for part in partiti:
                if conto_p>1:
                    break
                for i in tweet[u'ht']:
                    if i in final_dic[part]:
                        conto_p+=1
                        part_name=part
                        break
            if conto_p==1:
                collection.update({"_id":tweet['_id']},{'$set': {"tw_pr": part_name}})
                if us_tw_dic.has_key(int(tweet[u'user'])):
                    us_tw_dic[int(tweet[u'user'])].append(partiti.index(part_name))
                else:
                    us_tw_dic[int(tweet[u'user'])]=[partiti.index(part_name)]

        out.append("classified tweets:")
        print ("classified tweets:")
        out.append(collection.find({"tw_pr":{'$exists': True}}).count())
        print (collection.find({"tw_pr":{'$exists': True}}).count())
        #logging.info('tw '+str(collection.find({"tw_pr":{'$exists': True}}).count()))
        out.append(datetime.now().time())
        print (datetime.now().time())
        print ""

        #user_id=collection.find({"tw_pr":{'$exists': True}}).distinct("user")

        out.append("users classification")
        print ("users classification")


        pnt=0
        for i in us_tw_dic.keys():
            pnt+=1
            #if pnt%100000==0:
            #    print pnt
            list_part=us_tw_dic[i]
            most_list=mostcommon(list_part)
            if len(most_list)==1 or most_list[0][1]>(most_list[1][1])*2:
                us_dic[i]=most_list[0][0]

        #udic.append(us_dic)

        out.append("classified users:")
        print ("classified users:")
        out.append(len(us_dic.keys()))
        print (len(us_dic.keys()))
        out.append(datetime.now().time())
        print (datetime.now().time())
    #    print len(collection.find({"us_final":{'$exists': True}}).distinct("user"))
        #logging.info('us '+str(len(us_dic)))
        #print datetime.now().time()


        #H_list=[]
        #Edges=[]
        hash_score={}
        #param=0.002

        part_ht=[]
        part_ht_dict=[]
        out.append("")
        print ("")
        final_dic_b = final_dic.copy()


        for part in partiti:
            print part
            #print "graph construction"
            hashtag={}
            num_tot_tw=0
            for a in collection.find({"day": { "$gt": dlist[cic*ndays]-1, "$lt": end_d}}):
                if us_dic.has_key(int(a[u'user'])):
                    if us_dic[int(a[u'user'])]==partiti.index(part):
                        num_tot_tw+=1
                        parole=[]
                        for i in a[u'ht']:
                            parole.append(i)
                        for p in set(parole):
                            if hashtag.has_key(p.lower()):
                                hashtag[p.lower()]+=1
                            else:
                                hashtag[p.lower()]=1

    #         for q in polar_h:
    #             if hashtag.has_key(q):
    #                 del hashtag[q]

            list_hashtag=[(k,v) for v,k in sorted([(v,k) for k,v in hashtag.items()],reverse=True) if v>1]
            #hot_hashtag=[]
            list_hash=[]
            for i in list_hashtag:
                #hot_hashtag.append(i[0])
                list_hash.append(i[0])


            out.append('retrieved hashtags')
            print ('retrieved hashtags')
            out.append(len(list_hash))
            print (len(list_hash))
            out.append(datetime.now().time())
            print (datetime.now().time())

            #H=nx.Graph()
            #for i in mostcommon(edges):
                #H.add_edge(i[0][0], i[0][1],weight=i[1]/float(mostcommon(edges)[0][1]))
            #H_list.append(H)

            #exec("%s_upd=list_hash" % part)

            out.append("")
            print ("")


            for h in list_hash:
                if hashtag.has_key(h):
                    score=hashtag[h]/float(num_tot_tw)
                else:
                    score=0
    #             if h in eval(part):
    #                 score=1
    #             else:

    #                 calc2=0
    #                 for a in collection.find({"us_final2": part}):
    #                     if h in a[u'ht']:
    #                         if len(set(a[u'ht']).intersection(eval(part)))>0:
    #                             calc2+=1

    #                 val=calc2
    #                 score=round(val/float(hashtag[h] + calc1 - val),5)

                if hash_score.has_key(h):
                    hash_score[h][partiti.index(part)]=score

                else:
                    hash_score[h]=[]
                    for np in range(len(partiti)):
                        hash_score[h].append(0)

                    hash_score[h][partiti.index(part)]=score

            final_dic[part]=[]
            part_ht_dict.append({})
            #exec("%s=[]" % part)
            #exec("%sdic={}" % part)

        #part_ht=[]
        #part_ht_dict=[]

        #out.append(datetime.now().time())

        for k,v in hash_score.iteritems():
            max_h=max(v)
            cnt=v.index(max_h)
            v=filter(lambda a: a != max_h, v)
            if len(v)==(len(partiti)-1):
                kval=1
                for val_v in v:
                    kval=kval*(1-float(val_v))
                fscore=round(max_h*(kval),5)
                if fscore>param:
                    #print k
                    #print max_h
                    part=partiti[cnt]
                    #exec("%s.append(k)" % part)
                    #exec("%sdic[k]=fscore" % part)
                    final_dic[part].append(k)
                    part_ht_dict[partiti.index(part)][k]=fscore
        #print datetime.now().time()
        #for part in partiti:
        #    hdic.append(eval(part))

        for part in partiti:

            out.append('\n')
            print ('\n')
            out.append('TOPICS:')
            print ('TOPICS:')
            out.append(part)
            print (part)
            out.append(len(final_dic[part]))
            print (len(final_dic[part]))
            out.append([(k,v) for v,k in sorted([(v,k) for k,v in part_ht_dict[partiti.index(part)].items()],reverse=True)])
            print ([(k,v) for v,k in sorted([(v,k) for k,v in part_ht_dict[partiti.index(part)].items()],reverse=True)])
            if len(final_dic[part])==0:
                final_dic[part]=final_dic_b[part]
        out.append("")
        print ('')
        out.append('total tweets in period:')
        print ('total tweets in period:')
        out.append(collection.find({"day": { "$gt": dlist[cic*ndays]-1, "$lt": end_d}}).count())
        print (collection.find({"day": { "$gt": dlist[cic*ndays]-1, "$lt": end_d}}).count())
        out.append('total users in period:')
        print ('total users in period:')
        out.append(str(len(collection.find({"day": { "$gt": dlist[cic*ndays]-1, "$lt": end_d}}).distinct("user"))))
        print (str(len(collection.find({"day": { "$gt": dlist[cic*ndays]-1, "$lt": end_d}}).distinct("user"))))

        out.append("")
        print ('')

        #print collection.find().count()
        for part in partiti:
            out.append(part)
            print (part)
            out.append('polarized tweets: ' + str(collection.find({"tw_pr": part}).count()))
            print ('polarized tweets: ' + str(collection.find({"tw_pr": part}).count()))
            n2=len([i for i in us_dic.values() if i==partiti.index(part)])
            out.append('polarized users: ' + str(n2))
            print ('polarized users: ' + str(n2))
        out.append('\n')
        print ('\n')
        out.append('total polarized users: ' + str(len(us_dic)))
        print ('total polarized users: ' + str(len(us_dic)))
        out.append('\n')
        print ('\n')

        collection.update({}, {'$unset': {"tw_pr":1}}, multi=True)

    return out


import sys
from pymongo import MongoClient
from operator import itemgetter
from dateutil import parser
import ast
import numpy as nup
from datetime import datetime
import time

if __name__ == "__main__":

    client = MongoClient()

    exec("db = client." + sys.argv[1])

    exec("collection = db." + sys.argv[2])

    print ""

    print 'Number of arguments: ', len(sys.argv), 'arguments.'

    print 'Argument List: ', str(sys.argv)

    print ""

    print 'Database: ', str(sys.argv[1])

    print 'Collection: ', str(sys.argv[2])

    exec("file_or = '%s'" % sys.argv[3])

    exec("time_version = %s" % sys.argv[4])

    exec("iteration = %s" % sys.argv[5])

    exec("file_class = '%s'" % sys.argv[6])

    exec("param = %s" % sys.argv[7])

    param=float(param)
    #collection.remove({})

    with open(file_or, 'r') as f:
        cnt=0
        for line in f:
            if line[-1]=='\n':
                line=line[:-1]
            line=line.replace(': null', ': None')
            line=line.replace(': false', ': False')
            line=line.replace(': true', ': True')
            tw=ast.literal_eval(line)
            line2={}
            line2[u'user']=tw[u'user_id']
            line2[u'day']=parser.parse(tw['created_at']).year*10000+parser.parse(tw['created_at']).month*100+parser.parse(tw['created_at']).day
            line2[u'tw_id']=tw[u'id_str']
            ht=[]
            for i in tw[u'hashtags']:
                ht.append(i[u'text'].lower())
            line2[u'ht']=ht
            cnt+=1
            collection.insert(line2)
#
    print "Tweets inserted in MongoDB: ",str(cnt)
    if cnt!=collection.find().count():
       print "Error in MongoDB - partial data"

    final_dic=get_data(file_class)



    if time_version==0:
        out=polarization_track(collection, iteration, param, **final_dic)
    elif time_version==1:
        out=time_polarization_track(collection, iteration, param, **final_dic)
    else:
        print "Error in parameter: type of algorithm (time or not)"


    #for i in out:
    #   print str(i)
