#!/usr/bin/env python

def howmany(bit):
    """ how many values are we going to pack? """
    return 32
    #number = (64+bit-1)/bit
    #while((number * bit) % 8 != 0):
    #    number += 1
    #return number

def howmanywords(bit):
    return (howmany(bit) * bit + 63)/64

def howmanybytes(bit):
    if(howmany(bit) * bit % 8 <>0): raise "error"
    return (howmany(bit) * bit + 7)/8

print("""
/** code generated by superchargedpacking32.py starts here **/
/**
* this code mimics the way TurboPFor packs short arrays of integers.
* We pack and unpack always at least a full 64-bit word, plus whatever
* is necessary to get to an even number of bytes.
*/""")

print("""typedef void (*packblockfnc)(const uint32_t ** pin, uint8_t ** pw);""")
print("""typedef void (*unpackblockfnc)(const uint8_t ** pw, uint32_t ** pout);""")






def plurial(number):
    if(number <> 1):
        return "s"
    else :
        return ""

print("")
print("static void packblock0(const uint32_t ** pin, uint8_t ** pw) {");
print("  (void)pw;");
print("  *pin += {0}; /* we consumed {0} 32-bit integer{1} */ ".format(howmany(0),plurial(howmany(0))));
print("}");
print("")

for bit in range(1,33):
    print("")
    print("/* we are going to pack {0} {1}-bit values, touching {2} 64-bit words, using {3} bytes */ ".format(howmany(bit),bit,howmanywords(bit),howmanybytes(bit)))
    print("static void packblock{0}(const uint32_t ** pin, uint8_t ** pw) {{".format(bit));
    print("  uint64_t * pw64 = *(uint64_t **) pw;");
    print("  const uint32_t * in = *pin;");
    print("  /* we are going to touch  {0} 64-bit word{1} */ ".format(howmanywords(bit),plurial(howmanywords(bit))));
    for k in range(howmanywords(bit)) :
      print("  uint64_t w{0};".format(k))
    for j in range(howmany(bit)):
      firstword = j * bit / 64
      secondword = (j * bit + bit - 1)/64
      firstshift = (j*bit) % 64
      if( firstword == secondword):
          if(firstshift == 0):
            print("  w{0} = (uint64_t) in[{1}];".format(firstword,j))
          else:
            print("  w{0} |= (uint64_t)  in[{1}] << {2};".format(firstword,j,firstshift))
      else:
          print("  w{0} |= (uint64_t) in[{1}] << {2};".format(firstword,j,firstshift))
          secondshift = 64-firstshift
          print("  w{0} = (uint64_t) in[{1}] >> {2};".format(secondword,j,secondshift))
    for k in range(howmanywords(bit)) :
      print("  pw64[{0}] = w{0};".format(k))
    print("  *pin += {0}; /* we consumed {0} 32-bit integer{1} */ ".format(howmany(bit),plurial(howmany(bit))));
    print("  *pw += {0}; /* we used up {0} output bytes */ ".format(howmanybytes(bit)));
    print("}");
    print("")

print("static void unpackblock0(const uint8_t ** pw, uint32_t ** pout) {");
print("  (void) pw;");
print("  memset(*pout,0,{0});".format(howmany(0)));
print("  *pout += {0}; /* we wrote {0} 32-bit integer{1} */ ".format(howmany(0),plurial(howmany(0))));
print("}");
print("")

for bit in range(1,33):
    print("")
    print("/* we packed {0} {1}-bit values, touching {2} 64-bit words, using {3} bytes */ ".format(howmany(bit),bit,howmanywords(bit),howmanybytes(bit)))
    print("static void unpackblock{0}(const uint8_t ** pw, uint32_t ** pout) {{".format(bit));
    print("  const uint64_t * pw64 = *(const uint64_t **) pw;");
    print("  uint64_t * out = (uint64_t *) *pout;");
    maskval = (1<<bit)-1
    if(bit < 32): print("  const uint64_t masklow = UINT64_C({0});".format(hex(maskval)));
    masklowstr = " & masklow "
    if (bit == 32) : masklowstr = "" # no need
    maskval = (maskval << 32)
    if(bit < 32): print("  const uint64_t maskhigh = UINT64_C({0});".format(hex(maskval)));
    maskhighstr = " & maskhigh "
    if (bit == 32) : maskhighstr = "" # no need
    print("  /* we are going to access  {0} 64-bit word{1} */ ".format(howmanywords(bit),plurial(howmanywords(bit))));
    for k in range(howmanywords(bit)) :
      print("  uint64_t w{0} = pw64[{0}];".format(k))
    print("  *pw += {0}; /* we used up {0} input bytes */ ".format(howmanybytes(bit)));
    for k in range(howmany(bit)/2):
      j = 2*k
      firstword = j * bit / 64
      secondword = (j * bit + bit - 1)/64
      firstshift = (j*bit) % 64
      firstshiftstr = ">> {0} ".format(firstshift)
      if(firstshift == 0):
          firstshiftstr ="" # no need
      if( firstword == secondword):
          baseout = " ( w{0}  {1} ) ".format(firstword,firstshiftstr)
      else:
          secondshift = (64-firstshift)
          baseout = "  ( ( w{0} {1} ) | ( w{2} << {3} ) ) ".format(firstword,firstshiftstr, firstword+1,secondshift)
      baseout = "("+baseout + masklowstr+")"
      j = 2*k +1
      firstword = j * bit / 64
      secondword = (j * bit + bit - 1)/64
      firstshift = (j*bit) % 64
      firstshiftstr = "<< {0} ".format(32-firstshift)
      if(32-firstshift < 0):
        firstshiftstr = ">> {0} ".format(firstshift-32)
      if(32-firstshift == 0):
        firstshiftstr = " "
      if( firstword == secondword):
          highout = " ( w{1}  {2} ) ".format(j,firstword,firstshiftstr,firstshift)
      else:
          secondshift = (64-firstshift)
          secondshiftstr = " << {0} ".format(secondshift)
          highout = "    ( ( w{1} {2} ) | ( w{3} << {4} ) ) ".format(j,firstword,firstshiftstr, firstword+1,secondshift+32)
      highout = "("+highout + maskhighstr+")"
      print("  out[{0}] =  {1}  |  {2}  ; ".format(k,baseout,highout))
    print("  *pout += {0}; /* we wrote {0} 32-bit integer{1} */ ".format(howmany(bit),plurial(howmany(bit))));
    print("}");
    print("")

print("static packblockfnc funcPackArr[] = {")
for bit in range(0,32):
  print("&packblock{0},".format(bit))
print("&packblock32")
print("};")

print("static unpackblockfnc funcUnpackArr[] = {")
for bit in range(0,32):
  print("&unpackblock{0},".format(bit))
print("&unpackblock32")
print("};")
print("/** code generated by superchargedpacking32.py ends here **/")
