# Helmholtz coil
pi=3.14159
u0=4*pi*1e-7  #Tm/A

def hemB(n, R, B): #Helmolz coil
    I=B*R/(u0*n)*(0.8**(-3/2)) *1e-4
    print("current is", I, "A")
    I = round(I, 4)
    return I

def hemI(n, R, I): #Helmolz coil
    B=0.8**(3/2)*u0*n*I/R * 1e4
    print("Field is", B, "G")
    B = round(B, 4)
    return B

def coils(x, d, n, R, I, resi):  #general condition
    B1 = ((x-d/2)**2+R**2)**(-3/2)+((x+d/2)**2+R**2)**(-3/2)
    B = u0*n*I*R*R/2 * B1
    cc = u0*n*R*R/2 * B1 *1e4
    # print("coil constant", cc)
    # print("coil distance is ", d*100, 'cm')
    # print("field is ", B * 1e4 , "G")
    length = 2*pi*R*n #for each coil
    # print('wire length is: ', length,'m, ', length*3.28, 'ft')
    resis=length/304.8* resi *2    #2 coils parallel, AWG=12
    # print('wire resistance is: ', resis)
    # print('voltage is: ', resis*I, 'V')

    cc = round(cc, 4)
    B = round (B * 1e4, 4)
    lenm = round(length, 4)
    lenft = round(length*3.28, 4)
    vol = round(resis*1.3*I, 4)
    resis = round(resis*1.3, 4)

    return cc, B, lenm, lenft, vol, resis

if __name__ == "__main__":
    n = 135  # turns
    R = 7 * 0.01  # m radius cm

    B=20 *1e-4     #T field G
    I = hemB(n, R, B)
    # print(I)

    I = 10
    B = hemI(n, R, I)
    print(B)

    x=0 * 0.01 #m, x-axis cooridinate
    d=10 * 0.01     # m, distance between two coils
    I=1   #A  I<10A, U<20V
    resi=1.588

    cc, B, lenm, lenft, vol, resis = coils(x, d, n, R, I, resi)
    print(cc, B, lenm, lenft, vol, resis)


    #AWG 12, 29.49 g/m, diameter=2.05mm, 1.588 ohm/1000ft
    #AWG 13, 23.3 g/m, diameter=1.83mm, 2.003 ohm/1000ft