import copy
import sys
PLAIN = 0
MARKED = 1
CHOICE = 2


def max(matrix, dc=True):
    # Epilush tou prpvlhmatos anatheshs opou to sunoliko kostoso megistopoeihtai anti na elaxistopoeihtai
    # Arguments : matrix - mia lista me eisagwges n>=1, opou kathe n einai mia lista megethous n me stoixeieia mh arnhtikous arithmous
    # Epistrefei mia lista taksinomhmenwn zeygwn pou perigrafoun ta n pedia ta opoia megistopoihoun thn anathesh
    if dc:
        matrix = copy.dc(matrix)

    # "Anastrofh" tou pinaka etsi oste na xrhsimopoihthei h methodos elaxistopoihshs
    m = max(max(row) for row in matrix)
    for row in matrix:
        row[:] = map(lambda x: m - x, row)

    return min(matrix, False)
    # Telos tou max


def min(matrix, dc=True):
    # Epilush tou prpvlhmatos anatheshs opou to sunoliko kostos ths anatheshs elaxistopoeitai
    # Arguments : matrix - mia lista me eisagwges n>=1, opou kathe n einai mia lista megethous n me stoixeieia mh arnhtikous arithmous
    # Epistrefei mia lista taksinomhmenwn zeygwn pou perigrafoun ta n pedia ta opoia elaxistopoioun thn anathesh

    if dc:
        matrix = copy.dc(matrix)
    n = len(matrix)

    # Vhma 1
    # Gia kathe grammh tou pinaka, eyresh tou mikroterou stoixeiou kai afairesh tou apo to ekastote stoixeio ths idias grammhs.
    # Phgaine sto Vhma 2.
    for row in matrix:
        m = min(row)
        if m != 0:
            row[:] = map(lambda x: x - m, row)

    mask = [[PLAIN] * n for _ in matrix]
    row_cover = [False] * n
    col_cover = [False] * n

    # Vhma 2.
    # Vres 0 ston pinaka.
    # Ean den uparxei shmeiwmeno 0 se kapoia grammh\sthlh markare Z.
    # Epanalave gia kathe stoixeio tou pinaka.
    # Phgaine sto Vhma 3.
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if value == 0 and not row_cover[r] and not col_cover[c]:
                mask[r][c] = MARKED
                row_cover[r] = True
                col_cover[c] = True

    row_cover = [False] * n
    col_cover = [False] * n

    # Vhma 3
    # Kalupse kathe sthlh pou periexei shmeiwmno 0
    # Ean k sthles einai kalumenes, ta shmeiwmena 0, periografoun ena oloklhrwmeno set apo monadikes anatheseis.
    # Se auth th periptwsh oloklhrwthhke.
    # Alliws phgaine sto Vhma 4.

    match_found = False

    while not match_found:
        for i in range(n):
            col_cover[i] = any(mrow[i] == MARKED for mrow in mask)

        if all(col_cover):
            match_found = True
            continue
        else:
            # Vhma 4
            zero = _cover_zeroes(matrix, mask, row_cover, col_cover)

            # Vhma 5
            # Kataskeyh mia seira apo apo epilegmena k shmeiwmena 0 enalaks ws ekshs :
            # To Z0 antiproswpeuei ta mh kalumena epilegmena 0 pou vrethkan sto Vhma 4
            # To Z1 upodhlwnei ta shmeiwmena mhdenika sth sthlh tou Z0 (ean uparxoun)
            # To Z2 upodhlwnei ta shmeiwmena 0 sth grammh tou Z1(panta tha uparxei ena)
            # Sunexise mexri na teleiwsei h seira sto epilegmeno 0 etsi wste na mhn exei shmeiwmeno 0 sth sthlh tou.
            # Afairesh shmiwshs 0 apo th seira , shmeiwse kathe epilegmeno 0 sth seira
            # Diagrafh olwn twn epilegmenw kai mh kalumenwn se kathe grammh tou pinaka
            # Epistrofh sto Vhma 3.

            primes = [zero]
            stars = []
            while zero:
                for r, row in enumerate(mask):
                    if row[c] == MARKED:
                        zero = r, c
                else:
                    zero = None
                if zero:
                    stars.append(zero)
                    for c, val in enumerate(mask[r]):
                        if val == CHOICE:
                            zero =r, c
                    else:
                        zero = None
                    stars.append(zero)

            # Diagrafh shmeiwmenwn
            for star in stars:
                mask[star[0]][star[1]] = PLAIN

            # Shmeiwsh twn epilegmenwn
            for prime in primes:
                mask[prime[0]][prime[1]] = MARKED

            # Diagrafh twn upoloipwn epilegmenwn
            for r, row in enumerate(mask):
                for c, val in enumerate(row):
                    if val == CHOICE:
                        mask[r][c] = PLAIN

            row_cover = [False] * n
            col_cover = [False] * n
            # Telos tou vhmatos 5

        # Telos while vhmatos 3
    solution = []
    for r, row in enumerate(mask):
        for c, val in enumerate(row):
            if val == MARKED:
                solution.append((r, c))
    return solution
    # Telos tou min


# Methodos

def _cover_zeroes(matrix, mask, row_cover, col_cover):


    # Epanalhpsh vhmatwn 4 kai 6 mexri na mporesei na paei sto vhma 5
    while True:
        zero = True

        # Vhma 4
        # Vres mh kalumena 0 kai epelekse ta.
        # Ama den uparxoun shmeiwmena 0 sth grammh , sumperilmvanomenou tou sygkekrimenou epilegemenou 0,
        # phgaine sto Vhma 5,
        # Alliws kalupse ayth th grammh kai apokalupse thn sthlh pou periexei to shmeiwmeno 0
        # Sunexise me auton ton tropo mexri na mhn uparxoun alla akalupta 0
        # Apothhkeuse th mikroterh mh kalumenh timi kai phgaine sto Vhma 6.

        while zero:
            for r, row in enumerate(matrix):
                for c, value in enumerate(row):
                    if value == 0 and not row_cover[r] and not col_cover[c]:
                        zero=r, c
            else:
                zero=None
            if not zero:
                break  # sunexise sto Vhma 6
            else:
                row = mask[zero[0]]
                row[zero[1]] = CHOICE

                try:
                    index = row.index(MARKED)
                except ValueError:
                    return zero  # sunexise sto Vhma 5

                row_cover[zero[0]] = True
                col_cover[index] = False

        # Vhma 6
        # Prosthese thn aksia pou vrethhke sto vhma 4 se kathe stoixeio ths kathe kalumenhs grammhs kai
        # Afairese to apo kathe stoixeio ths kathe akalupths sthlhs
        # Epestrepse sto Vhma 4 xwris na allakseis kapoia shmeiwmenh,epilegmenh h kalymenh grammh


        for r, row in enumerate(matrix):
            for c, value in enumerate(row):
                if not row_cover[r] and not col_cover[c]:
                    m = value
        for r, row in enumerate(matrix):
            for c, __ in enumerate(row):
                if row_cover[r]:
                    matrix[r][c] += m
                if not col_cover[c]:
                    matrix[r][c] -= m
    # telos methodou
if __name__ == '__main__':

    c = sys.argv[1].split(' ') #-a
    c.strip().split(",")
    m = max(c)
    print(m)

    p = sys.argv[3].split(' ') #-m
    c.strip().split(",")
    p = min(p)
    print(p)
