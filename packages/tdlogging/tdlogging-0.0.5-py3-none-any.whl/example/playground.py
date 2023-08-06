from tdlogging.tdlogger import ApplyDecorators, RemoveDecorators

ApplyDecorators(target_dir="cool", import_root="example.logger_instance", var_name="logger", force=True)

for i in range(3):
    from example.cool.cooler.sleep import Sleep
    from example.cool.fib import Fib

    print(Fib.get_n(i))
    Sleep.sleep(1)

RemoveDecorators(target_dir="cool", import_root="example.logger_instance", var_name="logger", force=True)
