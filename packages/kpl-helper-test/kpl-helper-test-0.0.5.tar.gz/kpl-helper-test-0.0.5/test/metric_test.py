from kpl_helper import metric
figure = metric.MetricFigure("title", y1_name="loss")
iter_num = 100
for no in range(1, iter_num):
    ce_loss = 10.0 / no
    figure.push_metric(x=no, y1=ce_loss)


from kpl_helper.progress import send_progress
iter_num = 100
for no in range(1, iter_num):
    send_progress(float(no) / iter_num)
