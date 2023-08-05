# Flash-Bomb-Demo 春耕项目教学demo - 使用文档

**注意**：该工具只可用于**python 3**环境中。

# 使用方法

## Step: 检查文件夹结构

首先，一个完整的代码包，至少应包含下面的文件：

```.
├── flash_handler                   存放项目代码的文件夹
│   ├── config.py                   存放了一些常量，见后文
│   ├── const.py                    存放了一些常量，见后文
│   ├── excel_processor.py          存放用于操作Excel的基础模块
│   ├── file_keeper.py              存放用于维护文件列表的基础模块
│   ├── handler.py                                              存放中间逻辑，桥接基础模块和上层逻辑          
│   ├── spring.py                   存放上层逻辑
│   ├── static                                                        存放待操作eExcel文件的文件夹                 
│   │   ├── 闪光科技北京库存.xlsx      具体的待操作的Excel文件
│   │   ├── ...                             
│   └── utils.py                    存放工具类函数
└── requirements.txt                存放程序依赖的第三方库的名称和版本
```

请确保`spring.py`文件和`static`文件夹处在同一目录下。

## Step: 安装依赖项

在运行工具之前，需要确保工具所依赖的第三方库被正确安装。所需第三方库的名称及版本已经在`requirements.txt`中，可在终端内执行下面的命令以安装上相应的第三方库：

```
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r requirements.txt
```

注：`-i https://pypi.tuna.tsinghua.edu.cn/simple`可以让pip3工具是为了加快软件下载

## Step: 准备Excel文件

将待操作的Excel文件位于`static`文件，该文件夹下的其它Excel文件均可删除，以避免干扰。

由于`static`文件夹下允许存在多个Excel文件，请尽量让`static`文件夹下的Excel文件有相同的表头，以避免意外情况的发生。

## Step: 运行前检查

请确保Microsoft Excel、WPS等软件没有占用`static`文件夹下的任何一个Excel文件。

## Step: 运行

在终端中把当前目录切换到`spring.py`所在的目录，执行如下命令，即可使用工具：

```
python spring.py
```

# 文件内容描述

## 文件Config.py

存放程序所需的一些配置项。

    class Config(object):
          # 工作目录。程序将从此处获取Excel文件。
        DIR_PATH = os.getenv('FBD_DIR_PATH', 'static')
        
        # 邮箱设置
        SMTP_QQ_HOST = 'smtp.qq.com'
        SMTP_QQ_PORT = 587
        SMTP_MAIL_SUBJECT = 'python发送附件'
## 文件const.py

存放程序所需的一些常量。

    # 分隔符。如，用户输入多个数据时在不同数据间使用的分隔符。
    DELIMETERS = ',|，'
    
    # 图表种类的内部表示
    CHART_BAR_TYPE = 'bar'
    CHART_PIE_TYPE = 'pie'
    CHART_LINE_TYPE = 'line'
    
    # 图表种类对外展现的名称
    CHART_BAR_REPR = '柱状图'
    CHART_PIE_REPR = '饼图'
    CHART_LINE_REPR = '折线图'
    
    # 图表种类对外展现的名称和内部表示的映射关系
    CHART_REPR2TYPE = {
        CHART_BAR_REPR: CHART_BAR_TYPE,
        CHART_PIE_REPR: CHART_PIE_TYPE,
        CHART_LINE_REPR: CHART_LINE_TYPE,
    }
    
    # 图表纵坐标（柱状图或折线图）或统计量（饼图）计算方法的内部表示
    METHOD_SUM_TYPE = 'sum'
    METHOD_COUNT_TYPE = 'count'
    
    # 图表纵坐标（柱状图或折线图）或统计量（饼图）计算方法对外展现的名称
    METHOD_SUM_REPR = '加和'
    METHOD_COUNT_REPR = '计数'
    
    # 图表纵坐标（柱状图或折线图）或统计量（饼图）计算方法对外展现的名称和内部表示之间的映射关系
    METHOD_REPR2TYPE = {
        METHOD_SUM_REPR: METHOD_SUM_TYPE,
        METHOD_COUNT_REPR: METHOD_COUNT_TYPE,
    }
## 文件excel_processor.py

> 该文件包括操作Excel文件的基础模块及它所需要的辅助函数。

### 函数_setup_preferred_font()

> 设置合适的字体，使中文字符在图表中能正常显示。优先使用沙盒中存在的中文字体。

### 函数_setup_remedial_font()

> 设置合适的字体，使中文字符在图表中能正常显示。用于无法找到沙盒中存在的支持中文的字体的情况。

### 函数_setup_matplotlib()

> 设置字体（调用上面两个函数）。

### 类ExcelProcessor

> 用于操作单个Excel文件的基础模块，不存在与用户交互。

#### 方法search(file_path, primary_key, secondary_key)

> 根据主键primary_key和secondary_key，搜索位于路径file_path的Excel文件，并将搜索结果返回。

#### 方法append(file_path, values)

> 向位于路径file_path的Excel文件添加一行新的数据，数据的值由values指定。

#### 方法delete(file_path, row_indexes)

> 从位于路径file_path的Excel文件中删除一些行，具体哪些行由行的索引row_indexes指定。

#### 方法update(file_path, row_indexes, column_index, new_value)

> 修改位于路径file_path的Excel文件中的一些行，将这些行的指定列的取值更改为new_value。具体哪些行由行的索引row_indexes指定，具体哪一列由列的索引column_index指定。

#### 方法read_all(file_path)

> 读取位于路径file_path的Excel文件的所有数据并返回。

#### 方法read_headers(file_path)

> 读取位于路径file_path的Excel文件的表头并返回。

#### 方法draw_chart(cls, file_path, chart_type, horizontal_axis, vertical_axis, method, title, output_path

> 绘制图表。
>
> file_path：提供数据的Excel文件的路径
>
> chart_type：图表类型：柱状图、饼图、折线图
>
> horizontal_axis：Excel文件中用作横坐标的列名
>
> vertical_axis：Excel文件中用来计算图表纵坐标值（柱状图或折线图）或统计值（饼图）的列的名字
>
> method：计算纵坐标值（柱状图或折线图）或统计值（饼图）的方法：计数或加和
>
> title：图表标题
>
> output_path：图表保存的路径

#### 方法post_draw_line_chart(df, axis)

> 折线图特殊处理，用于调整折线图的刻度显示，使其与柱状图在样式上风格一致。
>
> df：数据源。
>
> axis：图表对象。

## 文件file_keeper.py

> 该文件包含了类FileKeeper及其实例。

### 类FileKeeper

> 文件“管家”。管理工作目录下的Excel文件列表和全部文件的列表。每个文件都有自己的索引。可用该索引获取文件名和文件路径，并进行相关操作。这是一个基础功能模块，不存在与用户交互。

#### 构造器_init__(self, dir_path)

> 构造该类的实例。

#### 方法refresh(self)

> 更新文件列表。

#### 属性all_files(self)

> 全部文件的列表。字典类型：键为索引，值为文件名。

#### 属性excel_files(self)

> 全部Excel文件的列表。字典类型：键为索引，值为文件名。

#### 方法get_file_path(self, index)

> 根据文件索引，获取文件的路径。

#### 方法print_excel_files(self, indexes=None)

> 打印所有Excel文件。可选参数indexes是文件索引，可以用于选择要打印的文件。

#### 方法print_all_files(self)

> 打印所有文件。

## 文件handler.py

### 函数_split(str_)

> 把用户输入的数据按分隔符分割。

### 函数_to_index_list(file_indexes)

> 把用户输入的文件索引转化成索引列表。

### 函数print_headers(file_path, prompt='')

> 打印位于file_path的Excel文件的表头。其中的prompt是打印在表头前的提示信息，默认为空。

### 函数print_match_detail(matches, primary_key, secondary_key)

> 打印以primary_key为主键、以secondary_key为次键的Excel查询结果的详细信息：查询命中的文件名和具体数据行。

### 函数print_match_summary(matches)

> 打印以primary_key为主键、以secondary_key为次键的Excel查询结果的概要信息：查询命中的文件名。

### 函数excel_search(primary_key, secondary_key='')

> 以主键primary_key和次键secondary_key对Excel文件进行搜索。所需要的其它信息会要求用户进行输入。其中的secondary_key为可选参数，默认为空字符串。

### 函数excel_files(path)

> 打印工作目录下的Excel文件名。参数path并无作用，只是为了满足`spring.py`的需要。

### 函数excel_add(file_indexes)

> 向索引file_indexes指定的Excel文件添加新的一行数据。所需要的其它信息会要求用户进行输入。

### 函数excel_delete(matches, file_indexes)

> 根据查询结果，对索引file_indexes指定的Excel文件进行删除操作。所需要的其它信息会要求用户进行输入。

### 函数excel_headers(file_indexes, prompt='表格的表头是: ')

> 打印file_indexes指定的Excel文件中第1个文件的表头。其中的prompt是打印在表头前的提示信息。

### 函数excel_update(matches, file_indexes, column)

> 根据查询结果matches，对文件索引file_indexes指定的Excel文件的列进行更新。具体是哪个列由参数column决定。所需要的其它信息会要求用户进行输入。

### 函数auto_picture()

> 绘制图表。所需要的信息会要求用户进行输入。

### 函数auto_email()

> 发送邮件。所需要的信息会要求用户进行输入。

## 文件spring.py

### 函数auto_add()

> 向工作目录下的部分或全部Excel文件添加新的一行数据，然后打印新增的行等信息。所需要的全部信息会要求用户进行输入。

### 函数auto_search()

> 对工作目录下的部分或全部Excel文件中的数据进行搜索，打印搜索结果。所需要的全部信息会要求用户进行输入。

### 函数auto_delete()

> 删除工作目录下的部分或全部Excel文件中符合特定条件的行，随后打印删除操作是否成功等结果信息。所需要的全部信息会要求用户进行输入。

### 函数auto_update()

> 对工作目录下的部分或全部Excel文件中符合特定条件的行，随后打印更新操作产生的效果等结果信息。所需要的全部信息会要求用户进行输入。

### 函数pro_controller()

> 入口函数。在终端上提供菜单，让用户选择欲进行的Excel操作，并调用相应函数（上面所列函数）。

## 文件Utils.py

> 包含工具类Utils。

### 类Utils

#### 方法to_chart_type(type_repr)

> 把图表种类对外展现的名称转化为内部表示。转化失败时返回None。

#### 方法to_method_type(type_repr)

> 把图表纵坐标（柱状图或折线图）或统计量（饼图）计算方法对外展现的名称转化为内部表示。转化失败时返回None。

#### 方法get_all_methods(delimeter='/')

> 把程序所支持的、图表纵坐标（柱状图或折线图）或统计量（饼图）的所有计算方法（计数或加和）对外展现的名称用分隔符连接起来，得到字符串供调用者进行打印。分隔符的默认值为`'/'`。

#### 方法send_mail(to_mail, from_mail, auth_code, body, file_paths=None)

> 以to_mail为目标邮箱、from_mail为发送人邮箱、auth_code为发送邮件所需要的授权码、body为邮件正文、file_paths为邮件附件，发送邮件。file_paths默认为`None`，表示邮件不带附件。

## 文件requirements.txt

存放程序依赖的第三方库的名称和版本。

通常只在安装依赖项时有用（见前面步骤），一般无需理会。

```
cycler==0.10.0
et-xmlfile==1.0.1
jdcal==1.4.1
kiwisolver==1.1.0
matplotlib==3.1.2
numpy==1.18.1
openpyxl==3.0.2
pandas==0.25.3
pyparsing==2.4.6
python-dateutil==2.8.1
pytz==2019.3
six==1.13.0
```

# 高级设置

如果不希望把Excel文件放在`static`文件夹中，可在终端中设置环境变量，将当前目录切换至`spring.py`文件所在文件夹。Linux/Mac下的具体命令是：

```
export FBD_DIR_PATH=Excel文件所在的路径
```

Windows下的具体命令是：

```
set FBD_DIR_PATH=Excel文件所在的路径
```

# 开发规范

## 安装

欲安装依赖项，可参考命令：
```
pip install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple 
```

## 代码规范

### flake8

检查代码规范符合程度：
```
flake8 .
```

如果使用了虚拟环境，可能需要使用：
```
flake8 . --exclude=env名称
```

### autopep8

尝试自动修复规范错误：
```
autopep8 -i --exclude spring.py -r .
```

## 单元测试


建议优先使用coverage方式，并通过它报告的覆盖率是否在90%左右，来判断程序功能是否异常。这是因为，目前的单测重点落在跑通功能，而没有对运行结果做过多的检测。也就是说，即使过程当中有一些错误，单测可能也不会报告出来。这时，如果覆盖率比较大，则过程当中很可能就没有出错。当然，以后应该把对结构的检测补上。


### 准备

环境变量准备：

项目使用dotenv从.env配置文件中读取环境变量。这些环境变量目前主要由开发自已用来单元测试，并没有面向用户。

当前可配置的环境变量如下：

```
FROM_MAIL=源邮箱地址
AUTH_CODE=认证码
TO_MAILS=目标邮箱地址
CC_MAILS=抄送邮箱地址
```

如果想通过环境变量更改“excel所在文件夹”，可参考前面“高级设置”。也可以写在.env中。


### unittest

执行整个测试文件中的测试
```
PYTHONPATH=. pytest
```

执行单个测试用例类
```
PYTHONPATH=. pytest flash_handler/tests/test_basic.py::TestSpring
```

执行单个测试用例类的方法
```
PYTHONPATH=. pytest flash_handler/tests/test_basic.py::TestSpring::test_auto_add
```

如果使用pipenv，可以在项目根目录执行如下命令：
```
pipenv run pytest
```

### coverage

用coverage跑单元测试：
```
coverage run --source . -m pytest
```

生成代码覆盖率概要信息：
```
coverage report -m
```

生成代码覆盖率html文件：
```
coverage html
```
随后，可在`htmlcov`文件夹中打开`index.html`，观看覆盖率数据。


# 上传至pypi？

## 主要参考
- [How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)

## 主要步骤

- 准备
  - 安装twine
    `pip install twine`
  - 在TestPyPI上注册账号。这里可用公司个人邮箱。其实自个儿邮箱也没问题，因为这个网站本身就是供发包人进行测试用的。
  - 在PyPI上注册账号。这里可用公司个人邮箱。
- 修改setup.py
  - 作者、邮箱、版本、license等
- 打包
  `python setup.py sdist`
- 测试打出的包
  - 检查包中文件：`tar tzf XXX-X.X.X.tar.gz`
  - 检查包的描述是否会在pypi上被正确地展示：`twine check dist/*`
  - 上传至TestPyPI进行测试
    - 上传命令：`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
    - 上传后，即可在TestPyPI上查看该包。
    - 在新的环境上测试包的安装和使用：
      - 可从TestPyPI上把包手动下载下来，方便用国内源。
      - 然后在终端中切换到包所在的文件夹，使用下面命令去安装:
        `pip install 下载下来的包名 -i https://pypi.tuna.tsinghua.edu.cn/simple`
      - 在终端或脚本中，用`from flash_handler import handler`来导入`handler`，对其进行测试。

## 注意

**千万别发⼀个不可⽤的包。**别的不说，pypi不允许名字重⽤。如果发了⼀个不可⽤包，下次发包时，版本号肯定得变（通常是变
⼤）。
