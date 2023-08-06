CFLAGS ?= -ggdb -g -Wall

TEST_SRC = $(wildcard test_*.c)
TEST_BIN = $(TEST_SRC:.c=)
C_DHE_INCLUDE = -I../../dhe/
test: $(TEST_BIN)
	for cmd in $(TEST_BIN) ; do ./$$cmd || exit 1 ; done

% : %.o
	$(CC) $(CFLAGS) $(C_DHE_INCLUDE) -o $@ $^ -lm -lcmocka
%.o: %.c
	$(CC) -c $(CFLAGS) $(C_DHE_INCLUDE) -o $@ $<
%.d: %.c
	@set -o pipefail; \
	$(CC) $(C_DHE_INCLUDE) -MM $< | sed -e 's|.*:|$(<:.c=.o):|' -e 's,\($*\)\.o[ :]*,\1.o $@ : ,g' > $@

#cmocka_utils.o: cmocka_utils.c
$(TEST_BIN): cmocka_utils.o

-include $(TEST_SRC:.c=.d)
