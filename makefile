TEST_CMD := uv run -m unittest discover -s modules -p "test_*.py"

test:
	@echo "Running tests..."
	$(TEST_CMD)

run:
	uv run main.py