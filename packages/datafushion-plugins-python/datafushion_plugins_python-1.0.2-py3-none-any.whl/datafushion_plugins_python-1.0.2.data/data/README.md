# DataFushion_Plugins_Python说明

## 1.简介

针对Python算法在DataFushion平台使用所给出的插件,主要用于规范化算法的输入输出

## 2.使用

- [x] Step1:引入datafushon包中的operation模块
- [x] Step2:使用资源管理器进行数据拆解处理,并在其中实现自己需要实现的业务算法逻辑

```python
from datafushion import operation, HandleInputDataStruct, HandleDataSet


if __name__ == '__main__':
    with operation() as destruction:  # type: HandleDataSet
        input_data_struct_list = destruction.input_data_struct_list
        param_map = destruction.param_map
        param_multiply = float(param_map['multiply'])

        data_result = []

        for input_data_struct in input_data_struct_list:  # type: HandleInputDataStruct
            file_input_mapping = input_data_struct.file_input_mapping
            data_list = input_data_struct.data_list
            field_x = file_input_mapping['x']
            field_y = file_input_mapping['y']
            for data in data_list:
                x = float(data[field_x])
                y = float(data[field_y])
                sum_result = param_multiply * (x + y)
                res = {
                    "sum": sum_result,
                    "x":   x,
                    "y":   y,
                }
                data_result.append(res)

        destruction.data_result = data_result
```

注意:

------

destruction为解构的`HandleDataSet`实体类，

------

input_data_struct_list中包含了输入数据的封装,其类型为List

其元素为`HandleInputDataStruct`类,包含的属性为file_type,file_path,file_input_mapping,data_list

算法需要使用的是file_input_mapping和data_list

data_list是输入数据的字典列表

file_input_mapping为输入数据字段的映射

------

param_map为算法的参数字典

------

在对数据进行业务算法处理完成后,需要将拆解的destruction中的data_result属性赋值为业务算法的最终数据结果