out.sql: all_data.csv proc_csv.py
	./proc_csv.py > $@

all_data.csv: proc_table.py proc_list.py proc_2001.py proc_text.py
	./proc_table.py > $@
	./proc_list.py >> $@
	./proc_2001.py >> $@
	./proc_text.py >> $@

.PHONY: clean
clean:
	rm -f all_data.csv out.sql
