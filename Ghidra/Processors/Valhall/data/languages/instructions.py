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

swizzles = (
    (32,
     (None, None),
     (None,),
     (".h0", "0,16"),
     (".h1", "16,16"),
     (".b0", "0,8"),
     (".b1", "8,8"),
     (".b2", "16,8"),
     (".b3", "24,8"),
     ),
    (16,
     (".h00", "0,16", "0,16"),
     (".h10", "16,16", "0,16"),
     (None, "0,16", "16,16"),
     (".h11", "16,16", "16,16"),
     (".b00", "0,8", "0,8"),
     (".b20", "16,8", "0,8"),
     (".b02", "0,8", "16,8"),
     (".b22", "16,8", "16,8"),
     (".b11", "8,8", "8,8"),
     (".b31", "24,8", "8,8"),
     (".b13", "8,8", "24,8"),
     (".b33", "24,8", "24,8"),
     (".b01", "0,8", "8,8"),
     (".b23", "16,8", "24,8"),
     )
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

        widen1       = (36,39)
        widen2       = (26,29)

        mod_explicit = (11,11)
        mod_shadow   = (12,12)
        mod_lod_mode = (13,15)
        mod_and      = (24,24)
        mod_seq      = (25,25)
        mod_dim      = (28,29)
        mod_sat      = (30,30)
        mod_rhadd    = (30,30)
        mod_restype  = (30,31)
        mod_cmp      = (32,34)
        mod_skip     = (39,39)
 
        D1           = (40,45)
        DM           = (46,47)

        op           = (48,56)
        op2          = (16,19)

        sr1_0        = (40,45)
        sr1_1        = (40,45)
        sr1_2        = (40,45)
        sr1_3        = (40,45)
        sr2_0        = (16,21)
        sr2_1        = (16,21)
        sr2_2        = (16,21)
        sr2_3        = (16,21)

        clamp        = (32,33)

        # TODO: Some of these can be removed?
        ofs          = (8,23) signed
        constant     = (8,39)
        sr_count     = (33,35)
        load_lane    = (36,38)
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

attach variables [ src1r src2r src3r src4r D1 sr1_0 sr2_0 ] [
% for reg in range(64):
        r${reg}
% endfor
];

% for sr in range(1, 4):
attach variables [ sr1_${sr} sr2_${sr} ] [
% for reg in range(sr, 64):
        r${reg}
% endfor
% for reg in range(sr):
        _
% endfor
];
% endfor

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

# TODO: 64-bit swizzles
% for bits, *patterns in swizzles:
% for widen, (name, *ranges) in enumerate(patterns):
<%
   if not len(ranges): continue
   name = f'^"{name}"' if name else ""
   size = 32 // len(ranges)
   code = ""
   for num, r in enumerate(ranges):
      assign = f"[{num*size},{size}]" if size != 32 else ""
      if r and int(r.split(",")[1]) == size:
         val = f"S{s}[{r}]"
      elif r:
         val = f"zext(S{s}[{r}])"
      else:
         val = f"S{s}"
      code += f"temp{assign} = {val}; "
 %>SW${s}_${bits}: S${s}${name} is S${s} & widen${s}=${widen} { local temp:4; ${code}export temp; }
% endfor

% endfor
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

SAT: "" is mod_sat=0 { export 0:1; }
SAT: ".saturate" is mod_sat=1 { export 1:1; }

RHADD: "" is mod_rhadd=0 { export 0:1; }
RHADD: ".rhadd" is mod_rhadd=1 { export 1:1; }

LOD_MODE: ".zero" is mod_lod_mode=0 { export 0:1; }
LOD_MODE: ".computed" is mod_lod_mode=1 { export 1:1; }
LOD_MODE: ".explicit" is mod_lod_mode=4 { export 4:1; }
LOD_MODE: ".computed_bias" is mod_lod_mode=5 { export 5:1; }
LOD_MODE: ".grdesc" is mod_lod_mode=6 { export 6:1; }

DIMENSION: ".1d" is mod_dim=0 { export 0:1; }
DIMENSION: ".2d" is mod_dim=1 { export 1:1; }
DIMENSION: ".3d" is mod_dim=2 { export 2:1; }
DIMENSION: ".cube" is mod_dim=3 { export 3:1; }

SHADOW: "" is mod_shadow=0 { export 0:1; }
SHADOW: ".shadow" is mod_shadow=1 { export 1:1; }

EXPLICIT: "" is mod_explicit=0 { export 0:1; }
EXPLICIT: ".explicit_offset" is mod_explicit=1 { export 1:1; }

SKIP: "" is mod_skip=0 { export 0:1; }
SKIP: ".skip" is mod_skip=1 { export 1:1; }

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
define pcodeop saturate;

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

:NOP is op=0x00 { }

# TODO: Calculate saturation: check if 64-bit computation == 32-bit computation?
# TODO: CLPER, also shaddx?

% for num, op, code in ((0, "IADD", "a + b"), (1, "ISUB", "a - b"), (0xa, "IMUL", "a * b"), (0xb, "HADD", "zext(RHADD == 0) * ((a & b) + ((a ^ b) >> 1)) + zext(RHADD == 1) * ((a | b) - (a ^ b) >> 1)")):
% for saturate in (0, 1):
<%
   if op == "HADD":
      mods = "^RHADD"
      mod_field = "& RHADD"
      code_s = code.replace(">>", "s>>")
      if saturate: continue
   else:
      mods = '^".saturate"' if saturate else ""
      mod_field = f"& mod_sat={saturate}"
      if saturate:
          code = f"saturate({code})"
      code_s = code
 %>

:${op}.u32${mods} DEST, SW1_32, SW2_32 is op=0xA0 & op2=${num} & DEST & DM & SW1_32 & SW2_32 ${mod_field} {
        local a = SW1_32; local b = SW2_32;
        Store(DEST, DM, ${code});
}

:${op}.s32${mods} DEST, SW1_32, SW2_32 is op=0xA8 & op2=${num} & DEST & DM & SW1_32 & SW2_32 ${mod_field} {
        local a = SW1_32; local b = SW2_32;
        Store(DEST, DM, ${code_s});
}

:${op}.s32${mods} DEST, SW1_32, SW2_32 is op=0x1A0 & op2=${num} & DEST & DM & SW1_32 & SW2_32 ${mod_field} {
        local a = SW1_32; local b = SW2_32;
        Store(DEST, DM, ${code_s});
}

:${op}.v2u16${mods} DEST, SW1_16, SW2_16 is op=0xA1 & op2=${num} & DEST & DM & SW1_16 & SW2_16 ${mod_field} {
        local temp:4; local a; local b;
        a = SW1_16[0,16]; b = SW2_16[0,16]; temp[0,16] = ${code};
        a = SW1_16[16,16]; b = SW2_16[16,16]; temp[16,16] = ${code};
        Store(DEST, DM, temp);
}

% endfor
% endfor

:FADD.f32 DEST^DC, AN1, AN2 is op=0xA4 & DEST & DC & DM & AN1 & AN2 {
        StoreClamp(DEST, DM, DC, AN1 f+ AN2);
}
:FADD.v2f16 DEST^DC, AN1.h, AN2.h is op=0xA5 & DEST & DC & DM & AN1.h & AN2.h {
        res:4 = 0;
        res[0,16] = AN1.h[0,16] f+ AN2.h[0,16];
        res[16,16] = AN1.h[16,16] f+ AN2.h[16,16];
        StoreClamp(DEST, DM, DC, res);
}

# TODO and, seq modifiers
:ICMP.u32^CMP^RESTYPE DEST, SW1_32, SW2_32, S3 is op=0xf0 & CMP & RESTYPE & DEST & SW1_32 & SW2_32 & S3 {
}

<%!
   sr_count = 0
   def make_sr(sec=False, reg=1, count=None):
      global sr_count
      if count == None:
         count = sr_count
      l = [f'sr{reg}_{x}' for x in range(count)]
      if sec:
         return " & ".join(l)
      else:
         return "@" + ":".join(l)
%>

% for count in range(1, 5):
<%
   global sr_count
   sr_count = count
 %>
% for st in range(1, 3):
SR${st}_${count}: ${make_sr(reg=st)} is ${make_sr(True, reg=st)} { export sr${st}_0; }
% endfor
% endfor

% for sr_count in range(1, 5):

:TEX^EXPLICIT^SHADOW^LOD_MODE^DIMENSION^SKIP ${make_sr()}, SR2_4, S1
is op=0x128 & EXPLICIT & SHADOW & LOD_MODE & DIMENSION & SKIP & ${make_sr(True)} & SR2_4 & S1 & sr_count=${sr_count} unimpl

% endfor

"""

try:
    print(Template(template).render(src_ranges=src_ranges, swizzles=swizzles))
except:
    print(exceptions.text_error_template().render())
