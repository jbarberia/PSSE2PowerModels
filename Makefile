
IFILE = casos/ver2526pid.sav
IFILE = casos/ver2526pin.sav
IFILE = casos/ver2526va.sav
IFILE = casos/inv25hr.sav
IFILE = casos/inv25pi.sav
IFILE = casos/inv25va.sav
OFILE = tmp

check_basic_data: build_pm
	julia scripts/check_basic_data.jl $(OFILE).json

build_pm: correcciones
	python scripts/caspy2pm.py $(OFILE).sav

correcciones:
	python scripts/corrections.py $(IFILE) $(OFILE).sav

clean:
	rm -f $(OFILE).json
	rm -f $(OFILE).sav
