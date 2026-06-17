clean:
	rm -rf proto/agen
gen:
	buf generate
run_be_1:
	uv run uvicorn app.z_server:app
run_be_2:
	uvicorn app.z_server:app --host=0.0.0.0 --port=8080
run_fe:
	npm run dev
run_client:
	uv run python client_test.py
# --
install:
	pip install -r requirements.txt
update_req:
	pip freeze > requirements.txt