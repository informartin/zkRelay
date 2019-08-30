# DLS : ZoKrates floor function
#
# Input: d <int>, q <int> (modulo P), wobei P deine Primzahl, der Körper in dem wir rechnen is also Z/PZ
#        in Z/PZ ist keine zahl (größer als p)
# Output: d//q
#
p = 21888242871839275222246405745257275088548364400416034343698204186575808495617


def floor(d, q):
    if q > d:
        return 0
    elif q == d:
        return 1
    else:
        multiple = q
        counter = 1
        for i in range(1, p):
            multiple = multiple + q
            if (multiple > d) != (multiple < q):
                return counter
            else:
                counter = counter + 1


print(floor(11, 2))
