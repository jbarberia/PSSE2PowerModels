
IFILE = casos/ver2526pid.sav
IFILE = casos/ver2526pin.sav
IFILE = casos/ver2526va.sav
IFILE = casos/inv25hr.sav
IFILE = casos/inv25pi.sav
IFILE = casos/inv25va.sav
OFILE = tmp

check_complete_solution: build_pm
	julia scripts/check_complete_solution.jl $(OFILE).sav $(OFILE).json

check_basic_data: build_pm
	julia scripts/check_basic_data.jl $(OFILE).json

build_pm: correcciones
	python scripts/caspy2pm.py $(OFILE).sav

correcciones:
	python scripts/corrections.py $(IFILE) $(OFILE).sav

build_sadi:
	python scripts/corrections.py casos/ver2526pid.sav json/ver2526pid.sav
	python scripts/corrections.py casos/ver2526pin.sav json/ver2526pin.sav
	python scripts/corrections.py casos/ver2526va.sav  json/ver2526va.sav
	python scripts/corrections.py casos/inv25hr.sav    json/inv25hr.sav
	python scripts/corrections.py casos/inv25pi.sav    json/inv25pi.sav
	python scripts/corrections.py casos/inv25va.sav    json/inv25va.sav
	
	python scripts/caspy2pm.py json/ver2526pid.sav
	python scripts/caspy2pm.py json/ver2526pin.sav
	python scripts/caspy2pm.py json/ver2526va.sav
	python scripts/caspy2pm.py json/inv25hr.sav
	python scripts/caspy2pm.py json/inv25pi.sav
	python scripts/caspy2pm.py json/inv25va.sav
	
	rm -f json/ver2526pid.sav
	rm -f json/ver2526pin.sav
	rm -f json/ver2526va.sav
	rm -f json/inv25hr.sav
	rm -f json/inv25pi.sav
	rm -f json/inv25va.sav

clean:
	rm -f $(OFILE).json
	rm -f $(OFILE).sav
