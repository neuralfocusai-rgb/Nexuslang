for n, l in enumerate(open('nexusshop/v19.nx'), 1):
    if l.count('"') % 2 == 1:
        print(n, l[:80])
