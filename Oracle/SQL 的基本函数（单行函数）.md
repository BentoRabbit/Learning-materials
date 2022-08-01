SQL 的基本函数（单行函数）

单行函数：仅对单行进行处理，为每行返回一个结果



单行函数

这些函数仅对单行进行处理，为每行返回一个结果。单行函数具有多种不同类型。将介绍以下几种函数：

• 字符

• 数字

• 日期

• 转换

• 常规

单行函数能进行：

Ø 处理数据项

接收一个或多个参数，用户提供的常量、变量值、列名、表达式

Ø 接受参数并返回一个值

Ø 作用于每个返回的行

Ø 为每行返回一个结果

Ø 可以修改数据类型

Ø 可以嵌套

Ø 接受参数，这些参数可是列，也可以是表达式



单行函数用于处理数据项。其接受一个或多个参数，并对查询返回的每一行返回一个值。

参数可以是下列对象之一：

• 用户提供的常量

• 变量值

• 列名

• 表达式

 

单行函数的特点包括：

Ø 对查询中返回的每一行进行处理

Ø 为每行返回一个结果

Ø 可能会返回一个与所引用类型不同的数据值

Ø 可能需要一个或多个参数

Ø 可用于 SELECT、WHERE 和 ORDER BY子句中；也可以嵌套。



单行函数的几种类型：

Ø 字符函数：接受字符输入，可以返回字符值和数字值

Ø 数字函数：接受数字输入，可以返回数字值

Ø 日期函数：对 DATE 数据类型的值进行处理（所有日期函数都会返回一个 DATE 数据类型的值，只有 MONTHS_BETWEEN 函数返回一个数字。）

Ø 转换函数：将值从一种数据类型转换为另一种数据类型

Ø 常规函数：NVL、NVL2 、NULLIF 、COALESCE 、CASE 、DECODE



字符函数



大小写字母转换函数

| Function              | Result     |
| --------------------- | ---------- |
| lower('SQL Course')   | sql course |
| upper('SQL Course')   | SQL COURSE |
| initcap('SQL Course') | Sql Course |



lower函数

```
SQL> select lower('SQL Course') from dual;

LOWER('SQL
----------
sql course
```



upper函数

```
SQL> select upper('SQL Course') from dual;

UPPER('SQL
----------
SQL COURSE

```



initcap函数

```
SQL> select initcap('SQL Course') from dual;

INITCAP('S
----------
Sql Course

```



字符处理函数

| Function                           | Result     |
| ---------------------------------- | ---------- |
| concat('Hello', 'World')           | HelloWorld |
| substr('HelloWorld',1,5)           | Hello      |
| length('HelloWorld')               | 10         |
| intstr('HelloWorld', 'W')          | 6          |
| lpad(salary, 10, '*')              |            |
| rpad(salary, 10, '*')              |            |
| replace('JACK and JUE', 'J', 'BL') |            |
| trim('H' from 'HelloWorld')        |            |



**concat函数**

将值连接在一起，需要注意的是CONCAT 函数中**只能使用两个参数，只能拼接2个字符串**

语法格式：

![IMG_256](SQL 的基本函数（单行函数）.assets/clip_image001.gif)

```
SQL> select concat('Hello','World') from dual;

CONCAT('HE
----------
HelloWorld

```



**substr函数**

提取确定长度的字符串

语法格式

![IMG_256](SQL 的基本函数（单行函数）.assets/clip_image001-1655108524650.gif)

```
SQL> select substr('ABCDEFG',1,4) str1,substr('ABCDEFG',-5,3) str2 from dual;

STR1 STR
---- ---
ABCD CDE

```

substr('String',1,3)---->Str 从第1位开始截取3位数



**INSTR函数**

查找指定字符串的数字位置

语法格式：

![IMG_256](SQL 的基本函数（单行函数）.assets/clip_image002.jpg)

```
SQL> select instr('t#i#m#r#a#n#','#') str1, instr('t#i#m#r#a#n#','#',3) str2, instr('t#i#m#r#a#n#','#',3,2) str3 from dual;

      STR1       STR2       STR3
---------- ---------- ----------
         2          4          6

```



**LENGTH函数**

以数字值的形式显示字符串的长度

语法格式：

![IMG_256](SQL 的基本函数（单行函数）.assets/clip_image001-1655108773312.gif)

length('String')---->6 长度

```
SQL> select length('ABCDEFG'),lengthb('中国') from dual;

LENGTH('ABCDEFG') LENGTHB('中国')
----------------- -----------------
                7                 6

```



**LPAD函数**

返回一个表达式，左边使用一个字符表达式填充到 n 个字符的长度

语法格式：

![IMG_256](SQL 的基本函数（单行函数）.assets/clip_image001-1655108852953.gif)

```
SQL> select lpad('dreamfly',10),lpad('dreamfly',10,'*') from dual;

LPAD('DREA LPAD('DREA
---------- ----------
  dreamfly **dreamfly

```



**RPAD函数**

返回一个表达式，右边使用一个字符表达式填充到 n 个字符的长度

语法格式：

![IMG_256](SQL 的基本函数（单行函数）.assets/clip_image001-1655108939869.gif)

rpad(676768,10,'*')右填充

```
SQL> select rpad('dreamfly',10),rpad('dreamfly',10,'*') from dual;

RPAD('DREA RPAD('DREA
---------- ----------
dreamfly   dreamfly**

```



**REPLACE函数**

用给定的字符替换搜索到的字符串

![IMG_256](SQL 的基本函数（单行函数）.assets/clip_image002-1655108972541.jpg)

```
SQL> select replace('JACK and JUE','J','BL') from dual;

REPLACE('JACKA
--------------
BLACK and BLUE

```



**TRIM函数**
截去字符串首字符或尾字符（或者两者都截去）（如果 trim_character或trim_source是一个字符文字，则必须将其放在单引号内）

![image-20220613163027743](SQL 的基本函数（单行函数）.assets/image-20220613163027743.png)

trim('m' from 'mmtimranm')---->timran

```
SQL> select trim('m' from 'mmmmmmdreamflymmmmm'), trim(leading 'm' from 'mmmmmmmdreamflymmmmm') from dual;

TRIM('M' TRIM(LEADING'
-------- -------------
dreamfly dreamflymmmmm

```

trim注意事项：

1.如果不声明leading|trailing|both，默认就是both

2.如果不声明trim_character，默认是空格

3.不能同时使用leading和trailing，可以选择both实现即去头双去尾或者嵌套

4.trim_character参数只允许包含一个字符，不支持多字符

5.使用ltrim和rtrim可以实现多字符





数值函数



**ROUND函数**

将列、表达式或值舍入到 n 位小数位，如果省略了n，则不保留小数位（如果 n 为负数，则会舍入小数点左边的数字）

对指定的值做四舍五入,round(p,s) s为正数时，表示小数点后要保留的位数，s也可以为负数，但意义不大。

语法格式：

![IMG_256](SQL 的基本函数（单行函数）.assets/clip_image001-1655109749402.gif)

round:按指定精度对十进制数四舍五入,如:

- round(45.923, 1),结果,45.9 
- round(45.923, 0),结果,46 
- round(45.923, -1),结果,50 

```
SQL> SELECT ROUND(45.923,2), ROUND(45.923,0),ROUND(45.923,-1) FROM DUAL;

ROUND(45.923,2) ROUND(45.923,0) ROUND(45.923,-1)
--------------- --------------- ----------------
          45.92              46               50
```



**TRUNC函数**

将列、表达式或值截断到 n 位小数位，如果省略了n，则n默认为零 

对指定的值进行截断，不舍入 trunc(p,s)

语法格式：

![IMG_256](SQL 的基本函数（单行函数）.assets/clip_image001-1655109978403.gif)

trunc:按指定精度截断十进制数,如:

- trunc(45.923, 1),结果,45.9 
- trunc(45.923),结果,45 
- trunc(45.923, -1),结果, 40

```
SQL> SELECT TRUNC(45.923,2), TRUNC(45.923),TRUNC(45.923,-1) FROM DUAL;

TRUNC(45.923,2) TRUNC(45.923) TRUNC(45.923,-1)
--------------- ------------- ----------------
          45.92            45               40
```

使用 TRUNC 函数

TRUNC 函数用于将列、表达式或值截断到 n 位小数位。

TRUNC 函数使用参数的方式与 ROUND 函数非常类似。如果第二个参数为 0 或者缺失，

则会将值截断为整数。如果第二个参数为 2，则会将值截断到 2 位小数位。相反，如果

第二个参数为 -2，则会将值截断到小数点左边 2 位。如果第二个参数为 -1，则将值截断

到小数点左边 1 位。

与 ROUND 函数一样， TRUNC 函数也可与日期函数一起使用。



**MOD函数**

使用 MOD 函数

MOD 函数将返回第一个参数除以第二个参数之后的余数。在幻灯片示例中，针对职务 ID

为 SA_REP 的所有雇员计算薪金除以 5,000 后的余数。

注： MOD 函数经常用于确定一个值是奇数还是偶数。 MOD 函数也是 Oracle 散列函数。

 

返回除法后的余数

语法格式：

![IMG_256](SQL 的基本函数（单行函数）.assets/clip_image001-1655110049798.gif)

```
SQL> select mod(100,12) from dual;

MOD(100,12)
-----------
          4

```





处理日期

SYSDATE函数

```
SELECT sysdate FROM dual;
```

与日期有关的运算

• 对日期加上或减去一个数字可以获得一个新的日期值。

• 将两个日期相减可以得出它们之间的天数。

• 将小时数除以 24 可以将小时添加到日期中。

因为日期在oracle里是以数字形式存储的，所以可对它进行加减运算，计算是以天为单位

| 操作           | 结果 | 说明                       |
| -------------- | ---- | -------------------------- |
| 日期 + 数字    | 日期 | 为日期添加若干天           |
| 日期 - 数字    | 日期 | 从日期中减轻若干天         |
| 日期 - 日期    | 天数 | 从一个日期中减去另一个日期 |
| 日期 + 数字/24 | 日期 | 为日期添加若干小时         |



时间格式

SQL>select to_date('2003-11-04 00:00:00' ,'YYYY-MM-DD HH24:MI:SS') FROM dual;

 

SQL> select sysdate+2 from dual;  //当前时间+2day

 

SQL> select sysdate+2/24 from dual;   //当前时间+2hour

 

SQL> select (sysdate-hiredate)/7 week from emp;  //两个date类型差，结果是以天为整数位的实数。



使用算术运算符处理日期



日期处理函数

MONTHS_BETWEEN 

计算两个日期之间的月数

MONTHS_BETWEEN(date1, date2)：计算date1 和date2 之间的月数。结果可以是正数，也可以是负数。如果date1 晚于 date2，则结果为正数；如果date1早于date2，则结果为负数。结果中的非整数部分代表月份的一部分。

SQL>select months_between('1994-04-01','1992-04-01') mm from dual;

 

查找emp表中参加工作时间>30年的员工

SQL>select * from emp where months_between(sysdate,hiredate)/12>30;

 

考点：很容易认为单行函数返回的数据类型与函数类型一致，对于数值函数类型而言的确如此，但字符和日期函数可以返回任何数据类型的值。比如instr函数是字符型的，months_between函数是日期型的，但它们返回的都是数值。



ADD_MONTHS

给日期增加月份

ADD_MONTHS(date, n)：将n 个日历月添加到date。n 的值必须为整数，但可以为负数。

SQL>select add_months('1992-03-01',4) am from dual;





LAST_DAY

日期当前月份的最后一天

LAST_DAY(date)：计算包含date 的月份的最后一天的日期。

SQL>select last_day('1989-03-28') l_d from dual;





NEXT_DAY

NEXT_DAY(date, 'char')：计算date 之后一周内下一个指定日('char') 的日期。char 的值可以是代表某一天的一个数字或者是一个字符串。

NEXT_DAY的第2个参数可以是数字1-7，分别表示周日--周六(考点），比如要取下一个星期六，则应该是：

SQL>select next_day(sysdate,7) FROM DUAL; 





ROUND日期函数和TRUNC日期函数

round(p,s)

ROUND(date[,'fmt'])：返回舍入到由格式样式fmt 指定的单位的date。如果省略格式样式fmt，则date 将舍入到最近的一天。

 

TRUNC(date[, 'fmt'])：返回包含时间部分的日期date，该日期已截断到由格式样式fmt 指定的单位。如果省略格式样式fmt，则 date 将截断到最近的一天

 

在日期中的应用，如何舍入要看具体情况，'fmt'是MONTH按30天计，应该是15舍16入，'fmt'是YEAR则按6舍7入计算。 

可以使用 ROUND 和 TRUNC 函数处理数字和日期值。在处理日期时，这些函数会将日期舍入或截断到指定的格式样式。因此，可以将日期舍入到最近的年份或月份。如果格式样式为 Month，则日期在 1-15 时，返回当前月份的第一天。日期在16-31 时，返回下一月份的第一天。如果格式样式为 Year，则月份在 1-6 时，返回当前年份的第一天。月份在7-12 时，返回下一年份的第一天。 

 

SQL>

SELECT empno, hiredate,

   round(hiredate,'MONTH') AS round,

   trunc(hiredate,'MONTH') AS trunc

 FROM   emp

 WHERE  empno=7844;

 

SQL>

SELECT empno, hiredate, 

   round(hiredate,'YEAR') AS round,

   trunc(hiredate,'YEAR') AS trunc

FROM emp

WHERE empno=7839;

 

 

 

 

 

2）DISTINCT(去重)限定词的用法：       //distinct貌似多行函数，严格来说它不是函数而是select子句中的关键字。

 

SQL> select distinct job from emp;     //消除表行重复值。

 

JOB

\---------

CLERK

SALESMAN

PRESIDENT

MANAGER

ANALYST

 

SQL> select distinct job,deptno from emp;  //重复值是后面的字段组合起来考虑的

 

JOB      DEPTNO

--------- ----------

MANAGER      20

PRESIDENT     10

CLERK         10

SALESMAN     30

ANALYST      20

MANAGER      30

MANAGER      10

CLERK       30

CLERK       20

 

 

 

5）处理空值的几种函数（见第四章）

6）转换函数TO_CHAR、TO_DATE、TO_NUMBER （见第三章）