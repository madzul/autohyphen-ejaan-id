-- mti-pola.lua: ganti pola pemenggalan bahasa Indonesia dengan pola MTI (LuaLaTeX).
-- Dipanggil oleh mti-unla.cls: mti_pola(<nomor \language indonesian>[, <berkas pola>])
-- Berkas pola bawaan hyph-id-mti.pat; opsi kelas polabaku memakai hyph-id-baku.tex (autohyphen-id).
function mti_pola(id, berkas)
  berkas = berkas or 'hyph-id-mti.pat'
  local f = kpse.find_file(berkas, 'tex') or kpse.find_file(berkas)
  if not f then
    texio.write_nl('term and log', 'mti-unla: ' .. berkas .. ' tidak ditemukan, memakai pola bawaan babel')
    return
  end
  local fh = io.open(f, 'r')
  local s = fh:read('*a')
  fh:close()
  s = s:gsub('%%[^\n]*', '')
  local pat = s:match('\\patterns%s*{(.-)}') or s
  local exc = s:match('\\hyphenation%s*{(.-)}')
  local l = lang.new(id)
  lang.clear_patterns(l)
  lang.patterns(l, pat)
  if exc then lang.hyphenation(l, exc) end
  texio.write_nl('term and log', 'mti-unla: pola pemenggalan dimuat dari ' .. f)
end
