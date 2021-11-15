from mako.template import Template
from mako import exceptions

src_ranges = (
    ("r", 0, 5),
    ("u", 0, 5),
    ("i", 0, 4),
    ("ts", 0, 2),
    ("id", 0, 4),
    ("t", 6, 7),
)

template = """
define endian=little;
define alignment=8;

define space ram type=ram_space size=8 default;
define space register type=register_space size=4;

define token opword (64)
% for src in range(1, 5):
<% base = (src - 1) * 8 %>
        src${src} = (${base},${base + 7})
% for n, s, e in src_ranges:
        src${src}${n} = (${base+s},${base+e})
% endfor
% endfor

        absneg1      = (38,39)
        absneg2      = (36,37)
        absneg3      = (34,35)
        absneg4      = (32,33)

        widen1_32    = (36,39)
        widen2_32    = (26,29)

        mod_and      = (24,24)
        mod_seq      = (25,25)
        mod_restype  = (30,31)
        mod_cmp      = (32,34)

        D1           = (40,45)
        DM           = (46,47)

        op2      = (16,19)

        clamp        = (32,33)

        ofs          = (8,23) signed
        constant     = (8,39)
        sr_count     = (33,35)
        load_lane    = (36,38)
        unsigned_skip = (39,39)
        op           = (48,56)
        imm_mode     = (57,58)
        action       = (59,61)
        do_action    = (62,62)
;

define register offset=0x00 size=4 [
% for reg in range(64):
        r${reg}
% endfor
];

define register offset=0x100 size=4 [
% for reg in range(64):
        u${reg}
% endfor
];

# TODO: Use program_counter
define register offset=0x200 size=8 [
        PC SP
];

define register offset=0x300 size=4 [
        tls_ptr tls_ptr_hi wls_ptr wls_ptr_hi
        lane_id core_id program_counter
];

attach variables [ src1r src2r src3r src4r D1 ] [
% for reg in range(64):
        r${reg}
% endfor
];

attach variables [ src1u src2u src3u src4u ] [
% for reg in range(64):
        u${reg}
% endfor
];

attach values [ src1i src2i src3i src4i ] [
        0x0 0xffffffff 0x7fffffff 0xfafcfdfe 0x1000000 0x80002000
        0x70605030 0xc0b0a090 0x3020100 0x7060504 0xb0a0908 0xf0e0d0c
        0x13121110 0x17161514 0x1b1a1918 0x1f1e1d1c 0x3f800000
        0x3dcccccd 0x3ea2f983 0x3f317218 0x40490fdb 0x0 0x477fff00
        0x5c005bf8 0x2e660000 0x34000000 0x38000000 0x3c000000
        0x40000000 0x44000000 0x48000000 0x42480000
];

attach variables [ src1ts src2ts src3ts src4ts ] [
        _ _ tls_ptr tls_ptr_hi _ _ wls_ptr wls_ptr_hi
];

attach variables [ src1id src2id src3id src4id ] [
        _ _ lane_id _ _ _ core_id _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
        _ _ _ _ _ program_counter _
];

DEST: D1^".mask0" is D1 & DM=0 { export D1; }
DEST: D1^".h0" is D1 & DM=1 { export D1; }
DEST: D1^".h1" is D1 & DM=2 { export D1; }
DEST: D1 is D1 & DM=3 { export D1; }

% for s in range(1, 5):

S${s}: src${s}r is src${s}r & src${s}t=0 { export src${s}r; }
S${s}: "`"^src${s}r is src${s}r & src${s}t=1 { export src${s}r; }
S${s}: src${s}u is src${s}u & src${s}t=2 { export src${s}u; }
S${s}: src${s}i is src${s}i & src${s}t=3 & imm_mode=0 { export src${s}i; }
S${s}: src${s}ts is src${s}ts & src${s}t=3 & imm_mode=1 { export src${s}ts; }
S${s}: src${s}id is src${s}id & src${s}t=3 & imm_mode=3 { export src${s}id; }

% if s < 3:

SW${s}_32: S${s} is S${s} & widen${s}_32<2 { export S${s}; }
SW${s}_32: S${s}^".h0" is S${s} & widen${s}_32=2 { temp:4 = zext(S${s}[0,16]); export temp; }
SW${s}_32: S${s}^".h1" is S${s} & widen${s}_32=3 { temp:4 = zext(S${s}[16,16]); export temp; }
SW${s}_32: S${s}^".b0" is S${s} & widen${s}_32=4 { temp:4 = zext(S${s}[0,8]); export temp; }
SW${s}_32: S${s}^".b1" is S${s} & widen${s}_32=5 { temp:4 = zext(S${s}[8,8]); export temp; }
SW${s}_32: S${s}^".b2" is S${s} & widen${s}_32=6 { temp:4 = zext(S${s}[16,8]); export temp; }
SW${s}_32: S${s}^".b3" is S${s} & widen${s}_32=7 { temp:4 = zext(S${s}[24,8]); export temp; }

% endif
% endfor

#AN$: S$ is S$ & absneg$=0 { export S$; }
#AN$: S$^".neg" is S$ & absneg$=1 { t:4 = 0:4 f- S$; export t; }
#AN$: S$^".abs" is S$ & absneg$=2 { t:4 = abs(S$); export t; }
#AN$: S$^".neg.abs" is S$ & absneg$=3 { t:4 = 0:4 f- abs(S$); export t; }

AN1: S1 is S1 & absneg1=0 { export S1; }
AN1: S1^".neg" is S1 & absneg1=1 { t:4 = 0:4 f- S1; export t; }
AN1: S1^".abs" is S1 & absneg1=2 { t:4 = abs(S1); export t; }
AN1: S1^".neg.abs" is S1 & absneg1=3 { t:4 = 0:4 f- abs(S1); export t; }

AN2: S2 is S2 & absneg2=0 { export S2; }
AN2: S2^".neg" is S2 & absneg2=1 { t:4 = 0:4 f- S2; export t; }
AN2: S2^".abs" is S2 & absneg2=2 { t:4 = abs(S2); export t; }
AN2: S2^".neg.abs" is S2 & absneg2=3 { t:4 = 0:4 f- abs(S2); export t; }

# TODO: Fix these
AN1.h: S1 is S1 & absneg1=0 { export S1; }
AN1.h: S1^".neg" is S1 & absneg1=1 { t:4 = 0:4 f- S1; export t; }
AN1.h: S1^".abs" is S1 & absneg1=2 { t:4 = abs(S1); export t; }
AN1.h: S1^".neg.abs" is S1 & absneg1=3 { t:4 = 0:4 f- abs(S1); export t; }

AN2.h: S2 is S2 & absneg2=0 { export S2; }
AN2.h: S2^".neg" is S2 & absneg2=1 { t:4 = 0:4 f- S2; export t; }
AN2.h: S2^".abs" is S2 & absneg2=2 { t:4 = abs(S2); export t; }
AN2.h: S2^".neg.abs" is S2 & absneg2=3 { t:4 = 0:4 f- abs(S2); export t; }

# Comparison bits: LT=1 EQ=2 GT=4 NE=8
CMP: ".eq" is mod_cmp=0 { export 2:1; }
CMP: ".gt" is mod_cmp=1 { export 4:1; }
CMP: ".ge" is mod_cmp=2 { export 6:1; }
CMP: ".ne" is mod_cmp=3 { export 8:1; }
CMP: ".lt" is mod_cmp=4 { export 1:1; }
CMP: ".le" is mod_cmp=5 { export 3:1; }
CMP: ".gtlt" is mod_cmp=6 { export 5:1; }
# TODO: What does total even do?
CMP: ".total" is mod_cmp=7 unimpl

RESTYPE: ".i1" is mod_restype=0 { export 1:4; }
RESTYPE: ".f1" is mod_restype=1 { export 0x3f800000:4; }
RESTYPE: ".m1" is mod_restype=2 { export 0xffffffff:4; }
RESTYPE: ".u1" is mod_restype=3 { export 0:4; }

macro Store(reg, mask, val) {
      maskv = (mask & 1) * 0xffff + (mask & 2) * 0x7fff8000;
      reg = (val & maskv) | (reg & ~maskv);
}

macro StoreClamp(reg, mask, clamp, val) {
      # if bit 1 is set, clamp to -1
      clamp_m1 = zext(val f> 0xbf800000:4) * val + zext(val f<= 0xbf800000) * 0xbf800000:4;
      val = zext((clamp & 1:1) != 0:1) * clamp_m1 + zext((clamp & 1:1) == 0:1) * val;

      # if bit 2 is set, clamp to 0
      clamp_0 = zext(val f> 0:4) * val + zext(val f<= 0) * 0:4;
      val = zext((clamp & 2:1) != 0:1) * clamp_0 + zext((clamp & 2:1) == 0:1) * val;

      # if bit 3 is set, clamp to 1
      clamp_1 = zext(val f> 0x3f800000:4) * 0x3f800000:4 + zext(val f<= 0x3f800000:4) * val;
      val = zext((clamp & 4:1) != 0:1) * clamp_1 + zext((clamp & 4:1) == 0:1) * val;

      Store(reg, mask, val);
}

DC: "" is clamp=0 { export 0:1; }
DC: ".clamp_0_inf" is clamp=1 { export 2:1; }
DC: ".clamp_m1_1" is clamp=2 { export 5:1; }
DC: ".clamp_0_1" is clamp=3 { export 6:1; }

define pcodeop clz;

:MOV.i32 DEST, S1 is op=0x91 & op2=0x0 & DEST & DM & S1 {
        Store(DEST, DM, S1);
}
:CLZ.i32 DEST, S1 is op=0x91 & op2=0x4 & DEST & DM & S1 {
        Store(DEST, DM, clz(S1));
}
:IABS.s32 DEST, S1 is op=0x91 & op2=0x8 & DEST & DM & S1 {
        Store(DEST, DM, zext(S1 s> 0) * S1 + zext(S1 s<= 0) * -S1);
}
:NOT.i32 DEST, S1 is op=0x91 & op2=0xE & DEST & DM & S1 {
        Store(DEST, DM, ~S1);
}

# TODO: Saturate
% for num, op, code in ((0, "IADD", "local temp = {} + {};"), (1, "ISUB", "local temp = {} - {};")):
:${op}.u32 DEST, SW1_32, SW2_32 is op=0xA0 & op2=${num} & DEST & DM & SW1_32 & SW2_32 {
        ${code.format("SW1_32", "SW2_32")}
        Store(DEST, DM, temp);
}
% endfor

:FADD.f32 DEST DC, AN1, AN2 is op=0xA4 & DEST & DC & DM & AN1 & AN2 {
        StoreClamp(DEST, DM, DC, AN1 f+ AN2);
}
:FADD.v2f16 DEST DC, AN1.h, AN2.h is op=0xA5 & DEST & DC & DM & AN1.h & AN2.h {
        res:4 = 0;
        res[0,16] = AN1.h[0,16] f+ AN2.h[0,16];
        res[16,16] = AN1.h[16,16] f+ AN2.h[16,16];
        StoreClamp(DEST, DM, DC, res);
}

# TODO and, seq modifiers
:ICMP.u32^CMP^RESTYPE DEST, SW1_32, SW2_32, S3 is op=0xf0 & CMP & RESTYPE & DEST & SW1_32 & SW2_32 & S3 {
}

"""

try:
    print(Template(template).render(src_ranges=src_ranges))
except:
    print(exceptions.text_error_template().render())
