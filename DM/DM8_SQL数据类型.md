# DM8_SQL数据类型

## 常规数据类型

### 数值数据类型

1. **NUMERIC** 

   用于存储零、正负定点数

2. **NUMBER** 

   与 NUMERIC 类型相同

3. **DECIMAL/DEC** 

   与 NUMERIC 类型相同

4. **BIT** 

   存储整数数据 1、0 或 NULL，可以用来支持 ODBC 和 JDBC 的布尔数据 类型

5. **INTEGER/INT** 

   存储有符号整数，精度为 10，标度为 0。

   取值范围为：-2147483648(- 2^31)～ +2147483647(2^31-1)。

6. **PLS_INTRGER** 

   与 INTEGER 相同

7. **BIGINT** 

   存储有符号整数，精度为 19，标度为 0。

   取值范围为：- 9223372036854775808(-2^63)～ 9223372036854775807(2^63-1)

8. **TINYINT** 

   用于存储有符号整数，精度为 3，标度为 0。取值范围为：-128～+127。

9. **BYTE** 

   与 TINYINT 相似，精度为 3，标度为 0

10. **SMALLINT** 

    存储有符号整数，精度为 5，标度为 0。

11. **BINARY ** 

    指定定长二进制数据，最大长度由数据库页 面大小决定，BINARY 常量以 0x 开始， 后跟数据的十六进制表示，例如 0x2A3B4058。

12. **VARBINARY** 

    指定变长二进制数据，用法类似 BINARY 数据类型

13. **REAL **

    带二进制的浮点数，但它不能由用户指定使用的精度，系统指定其二进制精 度为 24，十进制精度为 7。取值范围-3.4E + 38 ～ 3.4E + 38。

14. **FLOAT** 

    带二进制精度的浮点数，精度最大不超过 53，如省略精度，则二进制精度 为 53，十进制精度为 15。取值范围为-1.7E + 308 ～ 1.7E + 308。

15. **DOUBLE** 

    同 FLOAT 相似，精度最大不超过 53。

16. **DOUBLE PRECISION** 

    双精度浮点数，其二进制精度为 53，十进制精度为 15。取值范围-1.7E  + 308 ～ 1.7E + 308。



### 字符数据类型

1. **CHAR/CHARACTER** 

   定长字符串，最大长度由数据库页面大小决定，长度不足时，自动填充空格。

2. **VARCHAR** 

   可变长字符串，最大长度由数据库页面大小决定。



### 多媒体数据类型

1. **TEXT/LONGVARVHAR** 

   变长字符串类型，其字符串的长度最大为 2G-1，可用于存储长的文本串。

2. **IMAGE/LONGVARBINARY** 

   存储多媒体信息中的图像类型，图像由不定长的象素点阵组成，长度最大为 2G-1 字节，还可用于存储任何其它二进制数据。

3. **BLOB** 

   指明变长的二进制大对象，长度最大为 2G-1 字节。

4. **CLOB** 

   指明变长的字符串，长度最大为 2G-1 字节。

5. **BFILE** 

   指明存储在操作系统中的二进制文件，文件存储在操作系统而非数据库中， 仅能进行只读访问。



### 日期时间数据类型

1. **DATE** 

   包括年、月、日信息，定义了'-4712-01-01'和'9999-12-31'之间任 何一个有效的格里高利日期。

2. **TIME** 

   包括时、分、秒信息，定义了一个在'00:00:00.000000'和 '23:59:59.999999'之间的有效时间。TIME 类型的小数秒精度规定了秒字段中小数点 后面的位数，取值范围为 0～6，如果未定义，缺省精度为 0。

3. **TIMESTAMP/DATETIME** 

   包括年、月、日、时、分、秒信息，定义了一个在'- 4712-01-01 00:00:00.000000'和'9999-12-31 23:59:59.999999'之间的有效 格里高利日期时间。小数秒精度规定了秒字段中小数点后面的位数，取值范围为 0～6，如 果未定义，缺省精度为 6。

4. **TIME WITH TIME ZONE** 

   一个带时区的 TIME 值，其定义是在 TIME 类型的后面加上时区信息。取值范围：-12:59 与+14:00 之间。例 如：TIME '09:10:21 +8:00'。

5. **TIMESTAMP WITH TIME ZONE** 

   一个带时区的 TIMESTAMP 值，其定义是在 TIMESTAMP 类型的后面加上时区信息。取值范围：-12:59 与 +14:00 之间。例如：’2009-10-11 19:03:05.0000 -02:10’。

6. **TIMESTAMP WITH LOCAL TIME ZONE** 

   一个本地时区的 TIMESTAMP 值，能够将标准时区类型 TIMESTAMP WITH  TIME ZONE 类型转化为本地时区类型，如果插入的值没有指定时区，则默认为本地时区。

### BOOL/BOOLEAN数据类型

1. **BOOL **
2. **BOOLEAN**

布尔数据类型：TRUE 和 FALSE。如果变量或方法返回的类型是布尔类型，则返回值为 0 或 1。

TRUE 和非 0 值的返回值为 1，FALSE 和 0 值返回为 0。



## 记录类型

记录类型是由单行多列的标量类型构成复合类型，类似于 C 语言中的结构。记录类型提供了处理分立但又作为一个整体单元的相关变量的一种机制。

例如：DECLAREV_ID  INT; V_NAME VARCHAR(30); 这两个变量在逻辑上是相互关联的，因为它们分别对应 表 T(ID INT, NAME VARCHAR(30))中的两个字段。如果为这样的变量声明一个记录类 型，那么它们之间的关系就十分明显了。

定义记录类型的语法如下： 

```sql
TYPE <记录类型名> IS RECORD 
(<字段名><数据类型> [<default 子句>]{,<字段名><数据类型> [<default 子句>]});
<default 子句> ::= <default 子句1> | <default 子句2>
<default 子句1> ::= DEFAULT <缺省值> 
<default 子句2> ::= := <缺省值>
```

在 DMSQL 程序中使用记录，需要先定义一个RECORD 类型，再用该类型声明变量，也可以使用%ROWTYPE 来创建与表结构匹配的记录。

可以单独对记录中的字段赋值，使用点标记引用一个记录中的字段（记录名.字段名）。

例子：

```sql
DECLARE
	TYPE sale_person IS RECORD( 
		ID SALES.SALESPERSON.SALESPERSONID%TYPE, 
	SALESTHISYEARSALES.SALESPERSON.SALESTHISYEAR%TYPE); 
        v_rec sale_person;
BEGIN
	v_rec.ID := 1; 
	v_rec.SALESTHISYEAR:= 5500; 
	UPDATE SALES.SALESPERSON SET 			SALESTHISYEAR=v_rec.SALESTHISYEAR WHERE 
SALESPERSONID =v_rec.ID;

END;
/
```

也可以将一个记录直接赋值给另外一个记录，此时两个记录中的字段类型定义必须完全一致。

例子:

```sql
DECLARE
	TYPE t_rec IS RECORD (ID INT, NAME VARCHAR(50));
	TYPE t_rec_NEW IS RECORD( ID INT, NAME VARCHAR(50));
	v_rec1 T_REC;
	v_rec2 T_REC_NEW;
BEGIN
	SELECT PRODUCTID,NAME INTO v_rec1 FROM PRODUCTION.PRODUCT WHERE AUTHOR 
LIKE '鲁迅';
	v_rec2 := v_rec1;
	PRINT v_rec2.ID;
	PRINT v_rec2.NAME;
END;
/
```

定义记录类型时，字段的数据类型除了可以是常规数据类型，还可以是常规数据类型后跟着“[n]”或“[n1,n2...]”表示一维或多维数组。

例子：

```sql
DECLARE 
	TYPE T_REC IS RECORD( ID INT[3], NAME VARCHAR(30)[3]);
```

还支持定义包含数组、集合和其他 RECORD 的 RECORD。

例子：是一个 在 RECORD 定义中包含其他 RECORD 

```sql
DECLARE
	TYPE TimeType IS RECORD (hours INT, minutes INT ); 		  -- 定义记录TimeType
	TYPE MeetingType IS RECORD (
		day DATE,
		time_of TimeType   -- 嵌套记录TimeType 
); 
BEGIN
	NULL;
END;
/
```



## 数组类型

### 静态数组

**静态数组**是在声明时**已经确定了数组大小的数组**，其长度是预先定义好的，在整个程序中，**一旦给定大小后就无法改变**。

![image-20210716104702299](DM8_SQL数据类型.assets/image-20210716104702299.png)

定义了静态数组类型后需要用这个类型申明一个数组变量然后进行操作。

理论上 DM 支持静态数组的每一个维度的最大长度为 65534，但是静态数组最大长度 同时受系统内部堆栈空间大小的限制，如果超出堆栈的空间限制，系统会报错。

例子：

```sql
DECLARE
	TYPE Arr IS ARRAY VARCHAR[3];	-- TYPE 定义一维数组类型
	a Arr;	-- 声明一个二维数组
	TYPE Arr1 IS ARRAY VARCHAR[2,4];	-- TYPE定义二维数组类型
	b Arr1;	-- 声明一个二维数组
BEGIN
	FOR I IN 1..3 LOOP
		a[I] := I*10;
		PRINT a[I];
	END LOOP;
	PRINT '--------';
	
	FOR I IN 1..2 LOOP 
		FOR J IN 1..4 LOOP
			b[I][J] = 4*(I-1)+J;
			PRINT b[I][J];
		END LOOP;
	END LOOP;
	
END;
/
```



### 动态数组

动态数组可以随程序需要而**重新指定大小**，其内存空间是从堆 （HEAP）上分配（即动态分配）的，**通过执行代码而为其分配存储空间，并由 DM 自动释放内存。**

动态数组与静态数组的定义方法类似，区别只在于动态数组没有指定下标，需要动态分配空间。

定义动态数组类型的语法图例如下：

![image-20210716105620713](DM8_SQL数据类型.assets/image-20210716105620713.png)

定义了动态数组类型后需要用这个类型申明一个数组变量，之后在 DMSQL 程序的执行 部分需要为这个数组变量动态分配空间。

例子：

```sql
DECLARE
	TYPE Arr IS ARRAY VARCHAR[]; 
	a Arr; 
BEGIN
	a := NEW VARCHAR[4];  -- 动态分配空间
	FOR I IN 1..4 LOOP 
		a[I] := I * 4;
		PRINT a[I];
	END LOOP;
END;
/
```

对于多维动态数组，可以单独为每个维度动态分配空间。

例子：

```sql
DECLARE
	TYPE Arr1 IS ARRAY VARCHAR[,];
	b Arr1; 
BEGIN
	b := NEW VARCHAR[2][];	-- 动态分配第一维空间
	FOR I IN 1..2 LOOP 
		b[I] := NEW VARCHAR[4]; -- 动态分配第二维空间
		FOR J IN 1..4 LOOP
			b[I][J] = I*10+J;
			PRINT b[I][J];
		END LOOP;
	END LOOP;
END;
/
```

也可以一次性为多维动态数组分配空间，则上面的例子可以写为：

```sql
DECLARE
	TYPE Arr1 IS ARRAY VARCHAR[,];
	b ARR1; 
BEGIN
	b := NEW VARCHAR[2,4];
	FOR I IN 1..2 LOOP 
		FOR J IN 1..4 LOOP
			b[I][J]= I*10+J;
			PRINT b[I][J];
		END LOOP;
	END LOOP;
END;
/
```

理论上 DM 支持动态数组的每一个维度的最大长度为 2147483646，但是数组最大长度同时受系统内部堆空间大小的限制，如果超出堆的空间限制，系统会报错。



### 复杂类型数组

DM 还支持自定义类型、记录类型和集合类型的数组。

例子：定义了一个自定义类型（OBJECT 类型）的静态数组，存放图书的 序号和名称。

```sql
CREATE OR REPLACE TYPE COMPLEX AS OBJECT(
	RPART INT,
	IPART VARCHAR(100)
);
/
DECLARE
	TYPE ARR_COMPLEX IS ARRAY SYSDBA.COMPLEX[3]; 
	arr ARR_COMPLEX;
BEGIN
	FOR I IN 1..3 LOOP 
		SELECT SYSDBA.COMPLEX(PRODUCTID, NAME) INTO arr[I] FROM PRODUCTION.PRODUCT WHERE PRODUCTID=I;
		PRINT arr[I].RPART || arr[I].IPART;
	END LOOP;
END;
/
```

例子：定义了一个集合类型（以 VARRAY 为例）的数组，将员工的姓名、性别和 职位信息存放到数组变量中。

```sql
DECLARE 
	TYPE VARY IS VARRAY(3) OF varchar(100);
	TYPE ARR_VARY IS ARRAY VARY[8]; 
	arr ARR_VARY;
	v1,v2,v3 varchar(50);
BEGIN
	FOR I IN 1..8 LOOP 
		SELECT NAME,PERSON.SEX,TITLE INTO v1,v2,v3 FROM 
PERSON.PERSON,RESOURCES.EMPLOYEE WHERE PERSON.PERSONID=EMPLOYEE.PERSONID AND 
PERSON.PERSONID=I;
		arr[I] := VARY(v1,v2,v3);
		PRINT '*****工号'||I||'*****';
		FOR J IN 1..3 LOOP 
			PRINT arr[I][J];
 		END LOOP;
	END LOOP;
END;
/
```



## 集合类型

### VARRAY

VARRAY 是一种具有可伸缩性的数组，数组中的每个元素具有相同的数据类型。 VARRAY 在定义时由用户指定一个最大容量，其元素索引是从 1 开始的有序数字。

语法格式：`TYPE<数组名> IS VARRAY(<常量表达式>) OF <数据类型>；`

<常量表达式>表示数组的最大容量。

 <数据类型>是 VARRAY 中元素的数据类型，可以是常规数据类型，也可以是其他自定 义类型或对象、记录、其他 VARRAY 类型等，使得构造复杂的结构成为可能。

例子：查询人员姓名并将其存入一个 VARRAY 变量 中。VARRAY 最初的实际大小为 0

```sql
DECLARE
	TYPE MY_ARRAY_TYPE IS VARRAY(10) OF VARCHAR(100);
 	v MY_ARRAY_TYPE;
BEGIN
	v :=MY_ARRAY_TYPE();
	PRINT 'v.COUNT()=' || v.COUNT();
	FOR I IN 1..8 LOOP
		v.EXTEND();
		SELECT NAME INTO v(I) FROM PERSON.PERSON WHERE PERSON.PERSONID=I;
	END LOOP;
	PRINT 'v.COUNT()=' || v.COUNT();
	FOR I IN 1..v.COUNT() LOOP
		PRINT 'v(' || i || ')=' ||v(i);
	END LOOP;
END;
/
```



### 索引表

**索引表**提供了一种快速、方便地**管理一组相关数据的方法**。索引表是**一组数据的集合**，它**将数据按照一定规则组织起来**，形成一个可操作的整体，是对大量数据进行有效组织和 管理的手段之一，通过函数可以对大量性质相同的数据进行**存储、排序、插入及删除**等操作，从而可以有效地提高程序开发效率及改善程序的编写方式。 

索引表**不需要用户指定大小**，其**大小根据用户的操作自动增长**。

语法：`TYPE <索引表名> IS TABLE OF<数据类型> INDEX BY <索引数据类型>;`

例子：

```sql
DECLARE
	TYPE Arr IS TABLE OF VARCHAR(100) INDEX BY INT;
	x Arr;
BEGIN
	x(1) := 'TEST1';
	x(2) := 'TEST2';
	x(3) := x(1) || x(2);
	PRINT x(3);
END;
/
```



### 嵌套表

嵌套表不需要指定元素的个数，其大小可自动扩展。嵌套表元素的下标从 1 开始。

语法：`TYPE <嵌套表名> IS TABLE OF <元素数据类型>;`

元素数据类型用来指明嵌套表元素的数据类型，当元素数据类型为一个定义了某个表记录的对象类型时，嵌套表就是某些行的集合，实现了表的嵌套功能。

例子：子定义了一个嵌套表，其结构与 SALES.SALESPERSON 表相同，用来存放今年销售额大于 1000 万的销售代表的信息。

```sql
DECLARE
	TYPE Info_t IS TABLE OF SALES.SALESPERSON%ROWTYPE;
	info Info_t;
BEGIN
	SELECT SALESPERSONID,EMPLOYEEID,SALESTHISYEAR,SALESLASTYEAR BULK COLLECT 
INTO info FROM SALES.SALESPERSON WHERE SALESTHISYEAR>1000;

END;
/
```



### 集合类型支持的方法

DM 为 VARRAY、索引表和嵌套表提供了一些方法，用户可以使用这些方法访问和修改集合与集合元素。

1. COUNT

    语法： `<集合变量名>.COUNT`

    功能： 返回集合中元素的个数。 

2. LIMIT 

   语法：`<VARRAY 变量名>.LIMIT` 

   功能： 返回 VARRAY 集合的最大的元素个数，对索引表和嵌套表不适用。 

3. FIRST 

   语法： `<集合变量名>.FIRST` 

   功能： 返回集合中的第一个元素的下标号，对于 VARRAY 集合始终返回 1。

4. LAST 

   语法： `<集合变量名>.LAST` 

   功能： 返回集合中最后一个元素的下标号，对于 VARRAY 返回值始终等于 COUNT。 

5.  NEXT 

   语法： `<集合变量名>.NEXT(<下标>)` 

   参数： 指定的元素下标。 

   功能： 返回在指定元素 i 之后紧挨着它的元素的下标号，如果指定元素是最后一个元素，则返回NULL。 

6. PRIOR 

   语法： `<集合变量名>.PRIOR(<下标>)` 

   参数： 指定的元素下标。 

   功能： 返回在指定元素 i 之前紧挨着它的元素的下标号，如果指定元素是第一个元素，则返 回 NULL。 

7.  EXISTS 

   语法： `<集合变量名>.EXISTS(<下标>)` 

   参数： 指定的元素下标。 

   功能： 如果指定下标对应的元素已经初始化，则返回 TRUE，否则返回 FALSE。 

8. DELETE 

   语法： `<集合变量名>.DELETE([<下标>])` 

   参数： 待删除元素的下标。 

   功能： 下标参数省略时删除集合中所有元素，否则删除指定下标对应的元素，如果指定下标为 NULL，则集合保持不变。

9. DELETE 

   语法： `<集合变量名>.DELETE(<下标 1>, <下标 2>)` 

   参数： 下标 1：要删除的第一个元素的下标

   ​			下标 2：要删除的最后一个元素的下标 

   功能： 删除集合中下标从下标 1 到下标 2 的所有元素。

10. TRIM 

    语法： `<集合变量名>.TRIM([<n>])` 

    参数： 删除元素的个数。 

    功能： n 参数省略时从集合末尾删除一个元素，否则从集合末尾开始删除 n 个元素。本方法不适用于索引表。

11. EXTEND 

    语法： `<集合变量名>.EXTEND([])` 

    参数： 扩展元素的个数。 

    功能：n 参数省略时在集合末尾扩展一个空元素，否则在集合末尾扩展 n 个空元素。本方法不适用于索引表。

12.  EXTEND 

    语法： `<集合变量名>.EXTEND(,<下标>])`

    参数： n：扩展元素的个数

     		  下标：待复制元素的下标

    功能： 在集合末尾扩展 n 个与指定下标元素相同的元素。本方法不适用于索引表。



## 类类型

DM 支持类类型，类将结构化的数据及对其进行操作的过程或函数封装在一起。允许用户根据现实世界的对象建模，而不必再将其抽象成关系数据。关于类类型的详细介绍可以参考《DM8_SQL 语言使用手册》的相关章节。

DMSQL 程序中可以声明一个类类型的变量，初始化该变量后就可以访问类的成员变量， 调用类的成员方法了。



## 子类型

子类型是其基数据类型的子集。子类型具有与基数据类型相同的操作性质，但是其有效值域是基数据类型的子集。

语法：`SUBTYPE <subtype_name> IS <base_type> [(<精度>,[<刻度>])] [NOT NULL];`

例子：

```sql
DECLARE
	SUBTYPE COUNTER IS NUMBER(5);
	C COUNTER;
BEGIN
	NULL;
END;
```

该例子定义了一个名称为 COUNTER 的子类型，其实际数据类型为 NUMBER(5)。子类型可用来防止变量超出规定的值域，也可以增强 DMSQL 程序的可读性。

一旦定义了子类型，就 可以声明该类型的变量、常量等，如上例中的变量 C。



## 操作符

- 算术操作符

  | 操作符 | 对应操作 |
  | :----: | :------: |
  |   +    |    加    |
  |   -    |    减    |
  |   *    |    乘    |
  |   /    |    除    |

- 关系操作符

  | 操作符 | 对应操作 |
  | :----: | :------: |
  |   <    |   小于   |
  |   <=   | 小于等于 |
  |   >    |   大于   |
  |   >=   | 大于等于 |
  |   =    |   等于   |
  |   !=   |  不等于  |
  |   <>   |  不等于  |
  |  : =   |   赋值   |

- 比较操作符

  | 操作符  |           对应操作           |
  | :-----: | :--------------------------: |
  | IS NULL | 如果操作数为 NULL 返回 TRUE  |
  |  LIKE   |         比较字符串值         |
  | BETWEEN |     验证值是否在范围之内     |
  |   IN    | 验证操作数在设定的一系列值中 |

- 逻辑操作符

  | 操作符 |         对应操作         |
  | :----: | :----------------------: |
  |  AND   |    两个条件都必须满足    |
  |   OR   | 只要满足两个条件中的一个 |
  |  NOT   |           取反           |

