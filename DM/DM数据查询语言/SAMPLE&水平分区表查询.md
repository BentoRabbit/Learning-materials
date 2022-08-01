## SAMPLE 子句

DM 通过 SAMPLE 子句实现数据采样功能

```sql
-- 语法
<SAMPLE 子句>::=SAMPLE (<表达式>) |
SAMPLE (<表达式>) SEED (<表达式>) |
SAMPLE BLOCK (<表达式>) |
SAMPLE BLOCK (<表达式>) SEED (<表达式>)

-- 参数
1. <表达式>输入整数与小数均可；
2. SAMPLE (<表达式>) 按行采样 。 < 表达式 > 表 示 采 样 百分比，取值范围[0.000001,100)。重复执行相同语句，返回的结果不要求一致；
3. SAMPLE (<表达式>) SEED (<表达式>) 按行采样，并指定种子。其中 SEED(<表达式>)表示种子，取值范围[0,4294967295]。重复执行相同的语句，每次返回相
同的结果集；
4. SAMPLE BLOCK (<表达式>) 按块(页)采样。<表达式>表示采样百分比，取值范围[0.000001,100)。重复执行相同语句，返回的结果不要求一致，允许返回空集；
5. SAMPLE BLOCK (<表达式>) SEED (<表达式>) 按块(页)采样，并指定种子。其中，BLOCK (<表达式>)表示采样百分比，取值范围[0.000001,100)。SEED (<表达式>)表示种子，取值范围[0, 4294967295]。重复执行相同语句，每次返回相同的结果集。

                                                   -- 使用说明
1. SAMPLE 只能出现在单表或仅包含单表的视图后面；
2. 包含过滤条件的 SAMPLE 查询，是对采样后的数据再进行过滤；
3. 不能对连接查询、子查询使用SAMPLE 子句。
```

例：对PERSON.ADDRESS表按行进行种子为5的10%采样。 

```sql
SELECT * FROM PERSON.ADDRESS SAMPLE(10) SEED(5);
```





#  水平分区表查询

SELECT 语句从水平分区子表中检索数据，称水平分区子表查询，即<对象名>中使用的 是<分区表>。水平分区父表的查询方式和普通表完全一样。

```sql
-- 语法
<分区表>::=
[<模式名>.]<基表名> PARTITION (<一级分区名>) |
[<模式名>.]<基表名> SUBPARTITION (<多级子分区名>)

-- 参数
1. <基表名> 水平分区表父表名称；
2. <一级分区名> 水平分区表一级分区的名字；
3. <子分区名> 由水平分区表中多级分区名字逐级通过下划线"_"连接在一起的组合名称，例如 P1_P2_P3，其中 P1 是一级分区名、P2 是二级分区名、P3 是三级分区名。

-- 使用说明
如果 HASH 分区不指定分区表名，而是通过指定哈希分区个数来建立哈希分区表，PARTITIONS 后的数字表示哈希分区的分区数，使用这种方式建立的哈希分区表分区名是匿名的，DM 统一使用 DMHASHPART+分区号（从 0 开始）作为分区名。
```

例 1 查询一个 LIST-RANGE 三级水平分区表。

```sql
DROP TABLE STUDENT;
CREATE TABLE STUDENT(
NAME VARCHAR(20),
AGE INT,
SEX VARCHAR(10) CHECK (SEX IN ('MAIL','FEMAIL')),
GRADE INT CHECK (GRADE IN (7,8,9))
)
PARTITION BY LIST(GRADE)
 SUBPARTITION BY LIST(SEX) SUBPARTITION TEMPLATE
 (
 SUBPARTITION Q1 VALUES('MAIL'),
 SUBPARTITION Q2 VALUES('FEMAIL')
 ),
 SUBPARTITION BY RANGE(AGE) SUBPARTITION TEMPLATE
 (
 SUBPARTITION R1 VALUES LESS THAN (12),
 SUBPARTITION R2 VALUES LESS THAN (15),
 SUBPARTITION R3 VALUES LESS THAN (MAXVALUE)
 )
(
 PARTITION P1 VALUES (7),
 PARTITION P2 VALUES (8),
 PARTITION P3 VALUES (9)
);
SELECT * FROM STUDENT; --查询水平分区父表
SELECT * FROM STUDENT PARTITION(P1); -- 查询一级分区子表
SELECT * FROM STUDENT SUBPARTITION(P1_Q1); -- 查询二级分区子表
SELECT * FROM STUDENT SUBPARTITION(P1_Q1_R1); -- 查询三级分区子表
```

例2 查询一个指定HASH分区名的水平分区表。

```sql
CREATE TABLESPACE TS1 DATAFILE 'TS1.DBF' SIZE 128;
CREATE TABLESPACE TS2 DATAFILE 'TS2.DBF' SIZE 128;
CREATE TABLESPACE TS3 DATAFILE 'TS3.DBF' SIZE 128;
CREATE TABLESPACE TS4 DATAFILE 'TS4.DBF' SIZE 128;
DROP TABLE CP_TABLE_HASH CASCADE;
CREATE TABLE CP_TABLE_HASH(
C1 INT,
C2 VARCHAR(256),
C3 DATETIME,
C4 BLOB
)
PARTITION BY HASH (C1)
SUBPARTITION BY HASH(C2)
SUBPARTITION TEMPLATE
(SUBPARTITION PAR1 STORAGE (ON MAIN),
SUBPARTITION PAR2 STORAGE (ON TS1),
SUBPARTITION PAR3 STORAGE (ON TS2),
SUBPARTITION PAR4)
(PARTITION PAR1 STORAGE (ON MAIN),
PARTITION PAR2 STORAGE (ON TS1),
PARTITION PAR3 STORAGE (ON TS2),
PARTITION PAR4)
STORAGE (ON TS4) ;
SELECT * FROM CP_TABLE_HASH PARTITION(PAR1); -- 查询一级分区子表
SELECT * FROM CP_TABLE_HASH SUBPARTITION(PAR1_PAR1); -- 查询二级分区子表
```

例 3 查询一个指定 HASH 分区数的水平分区，查询 CP_TABLE_HASH01 第一个分区的数据。

```sql
DROP TABLE CP_TABLE_HASH01 CASCADE;
CREATE TABLE CP_TABLE_HASH(
C1 INT,
C2 VARCHAR(256),
C3 DATETIME,
C4 BLOB
)
PARTITION BY HASH (C1)
PARTITIONS 4 STORE IN (TS1, TS2, TS3, TS4);
SELECT * FROM CP_TABLE_HASH PARTITION (DMHASHPART0); -- 查询一级分区子表
```

