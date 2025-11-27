def st_subscribe_quote(recver, strategies):
    for st in strategies:
        recver.AddSubscriber(st)
    recver.StartReceive("MXFR1")