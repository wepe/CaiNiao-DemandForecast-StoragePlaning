/*全国数据合并*/
CREATE TABLE train_all AS
SELECT * FROM(
SELECT * FROM train_all_window1
UNION ALL
SELECT * FROM train_all_window2
UNION ALL
SELECT * FROM train_all_window3
UNION ALL
SELECT * FROM train_all_window4
UNION ALL
SELECT * FROM train_all_window5
UNION ALL
SELECT * FROM train_all_window6
UNION ALL
SELECT * FROM train_all_window7
UNION ALL
SELECT * FROM train_all_window8
UNION ALL
SELECT * FROM train_all_window9
UNION ALL
SELECT * FROM train_all_window10
)a;

/*分仓数据合并*/
CREATE TABLE train_fencang AS
SELECT * FROM(
SELECT * FROM train_fencang_window1
UNION ALL
SELECT * FROM train_fencang_window2
UNION ALL
SELECT * FROM train_fencang_window3
UNION ALL
SELECT * FROM train_fencang_window4
UNION ALL
SELECT * FROM train_fencang_window5
UNION ALL
SELECT * FROM train_fencang_window6
UNION ALL
SELECT * FROM train_fencang_window7
UNION ALL
SELECT * FROM train_fencang_window8
UNION ALL
SELECT * FROM train_fencang_window9
UNION ALL
SELECT * FROM train_fencang_window10
)a;