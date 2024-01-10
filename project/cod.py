def gen_adaptable_pathway(individual):
    #p1
    pathway = [] #a1
    #p2
    coord = MAZE_START#a2
    #p3
    pathway.append(coord)#a3
    #p4
    last_tried_dir = []#a4
    #p5
    coming_direction = None#a5
    #p6
    #a6 (i=0)
    #I
    for i in range(len(individual)):#c1 #functia de terminare1
        #p7
        row, col = coord#a7
        #p8
        gen = individual[i]#a8
        #p9
        direction = det_direction(gen)#a9
        #p10
        if direction in last_tried_dir:#c2
            #p11
            temp_dir = get_rand_dir_different_from(last_tried_dir)#a10
            #p12
            if temp_dir != UNBLOCK:#c21
                #p13
                direction = temp_dir#a11
            else:
                #p14
                direction = coming_direction#a12
        #p15
        if direction == RIGHT:#c3
            #p16
            if col + 1 == MAZE_SIZE:#C31 #functia de terminare2
                #p17
                col += 1#a12
                break
            #p18
            if maze[row][col + 1] == PATH:#c32
                #p19
                col += 1#a13
                #p20
                last_tried_dir = [LEFT]#a14
                #p21
                coming_direction = LEFT#a15
                #p22
                individual[i - (len(last_tried_dir))] = det_angle_based_on(direction)#a16
            elif maze[row][col + 1] == WALL:#c33
                #p23
                last_tried_dir.append(RIGHT)#a17
        elif direction == LEFT:#c4
            #p24
            if col - 1 >= 0:#c41
                #p25
                if maze[row][col - 1] == PATH:#C41
                    #p26
                    col -= 1#a18
                    #p27
                    last_tried_dir = [RIGHT]#a19
                    # p28
                    coming_direction = RIGHT#a20
                    # p29
                    individual[i - (len(last_tried_dir))] = det_angle_based_on(direction)#a21
                elif maze[row][col - 1] == WALL:#C42
                    #p30
                    last_tried_dir.append(LEFT)#a22
            else:
                #p31
                last_tried_dir.append(LEFT)#a23
        elif direction == UP:#C5
            #p32
            if maze[row - 1][col] == PATH:# C51
                #p33
                row -= 1#a24
                #p34
                last_tried_dir = [DOWN]#a25
                #p35
                coming_direction = DOWN#a26
                #p36
                individual[i - (len(last_tried_dir))] = det_angle_based_on(direction)#a26
            elif maze[row - 1][col] == WALL:# C52
                #p37
                last_tried_dir.append(UP)#a27
        elif direction == DOWN:#C6
            #p38
            if maze[row + 1][col] == PATH:# C61
                #p39
                row += 1#a28
                #p40
                last_tried_dir = [UP]#a29
                #p41
                coming_direction = UP#a30
                #p42
                individual[i - (len(last_tried_dir))] = det_angle_based_on(direction)#a31
            elif maze[row + 1][col] == WALL:# C62
                #p43
                last_tried_dir.append(DOWN)#a32
        #p44
        coord = (row, col)#a33
        #p45
        pathway.append(coord)#a34
        #p46
        #a35  (i++)
        #p47
    #pfinal
    return pathway, individual

#Preconditii: individ a[n], n > 0, a[i] apartine intervalului[0,360],i apartine intervalului[0,n-1]
#maze este o matrice de tip mxm, m > 0, maze[i][j] apartine {PATH, WALL}, i,j apartin intervalului[0,m-1]

#Postconditii: drumul path[n+1], path[i] este sub (x,y) x si y aparatinand[0,m-1] ,m = marimea maze-ului, i apartine intervalului[0,n]
# si  maze[path[i].x][path[i].y] = PATH
#invariantul e pathway

#Demonstratie  invariant:
    #Ipoteza
    #P(n): pathway are drumul parcurs de individ pana in pasul n

    #P(1) e adevarat ( prima coordonata din path este startul labirintului si este path)

    #P(k) (s-a ajuns la a k-a gena din individ si s-au adaugat k coordonate care sunt path la pathway)

    #Demonstrati ca P(k)->P(k+1)

    #Pornind de la pasul P(k) pornesc o noua iteratie in care salvez ultimele coordonate calculate in 2 variabile temporare x si y, daca directia curenta
# se afla in ultimele directii incercate se va schimba cu o una care nu a fost incercata, daca toate au fost incercate, individul primeste directia din care
#a venit (acesta primeste directia din care a venit doar daca a incercat toate directiile posibile). Mai departe se verifica urmatoarea coordonata,
# daca este zid, se adauga intr-o lista aceasta directie, daca este drum liber, se actualizeaza coordonatele, se actualizeaza directia de venire, se actualizeaza
#lista de incercari si se modifica individul pentru a evita pe viitor blocarea.La sfarsitul acesttor verificari, se adauga in pathway noua coordonata si se actualizeaz
#indexul,astfel avem k+1 elemente in pathway ajungand ca P(k+1)
    #Deci P(k)->P(k+1) adevarat (prin aplicarea unei iteratii asupra lui P(k) am ajuns la P(k+1))
    #Avand P(1) adevarat si inductia P()->P(k+1) corecta => P(n) e adevarat

#Demonstratie formala:
#p -> p1
#p1 & a1 = p2
#p2 & a2 = p3
#p3 & a3 = p4
#p4 & a4 = p5
#p5 & a5 = p6
#p6 & a6 = I
#I & c1 = p7
#I & !c1=pfinal
#p7 & a7 = p8
#p8 & a8 = p9
#p9 & a9 = p10
#p10 & c2 = p11
#p10 & !c2 = p17
#p11 & a10 = p12
#p12 & c21 = p13
#p12 & !c21 = p15
#p13 & a11 = p15
#p14 & a12 = p15
#p15 & c3=p16
#p16 & c31=p17
#p17 & a12=pfinal
#p16 & !c31=p18
#p18 & c32 =p19
#p19 & a13=p20
#p20 & a14=p21
#p21 & a15=p22
#p22 & a16=p44
#p18 & !c32 & c33=p23
#p23 & a17=p44
#
#p15 & !c3 & c4=p24
#p24 & c41=p25
#p25 & c41=p26
#p26 & a18=p27
#p27 & a19=p28
#p28 & a20=p29
#p29 & a21=p44
#p25 & !c41 & c42=p30
#p30 & a22=p44
#p24 & !c41 & !c42=p31
#p31 & a23=p44
#
#p15 & !c3 & !c4 & c5=p32
#p32 & c51=p33
#p33 & a24=p34
#p34 & a25=p35
#p35 & a26=p36
#p36 & a26=p44
#p33 & !c51 & c52=p37
#p37 & a27=p44
#
#p15 & !c3 & !c4 &!c5 &c6=p38
#p38 & c61=p39
#p39 & a28=p40
#p40 & a29=p41
#p41 & a30=p42
#p42 & a31=p44
#p39 & !c61 & c62=p43
#p43 & a32=p44
#
#p15 & !c3 & !c4 &!c5 &!c6=p44
#p44 & a=p45
#p45 & a=p46
#p46 & a=p47
#p47 & c1=p7
#p47 & !c1=pfinal


