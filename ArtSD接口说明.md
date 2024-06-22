---
title: 创新综合实践 ArtSD
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.23"

---

# 创新综合实践 ArtSD

Base URLs:

# Authentication

# Default

## GET 获取历史列表

GET /history

> Body 请求参数

```yaml
page: 0
page_size: 0

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Sn|header|string| 是 |none|
|body|body|object| 否 |none|
|» page|body|integer| 是 |none|
|» page_size|body|integer| 是 |none|

> 返回示例

> 成功

```json
{
  "code": 0,
  "data": {
    "page": 1,
    "page_size": 2,
    "pathlist": [
      {
        "id": "6665d018e7f947258b12be54",
        "processed_url": "/productions/2024/06/09/c4561ecce5c34c489bf1e34846e6d5a7demo2.jpg",
        "raw_url": "/uploads/2024/06/09/f1c6392a28d74eeca08b0490df7f1680demo2.jpg",
        "static": "anime"
      },
      {
        "id": "6665cfcee7f947258b12be53",
        "processed_url": "/productions/2024/06/09/3d824211c6664e4ca51a813a81d0e0fedemo2.jpg",
        "raw_url": "/uploads/2024/06/09/cef0df5dba3843e3986dce1759b13e0cdemo2.jpg",
        "static": "anime"
      }
    ],
    "total_documents": 3,
    "total_pages": 2
  },
  "msg": "ok"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|object|true|none||none|
|»» page|integer|true|none||none|
|»» page_size|integer|true|none||none|
|»» pathlist|[object]|true|none||none|
|»»» id|string|true|none||none|
|»»» processed_url|string|true|none||none|
|»»» raw_url|string|true|none||none|
|»»» static|string|true|none||none|
|»» total_documents|integer|true|none||none|
|»» total_pages|integer|true|none||none|
|» msg|string|true|none||none|

## POST 获取风格列表

POST /stylelist

> Body 请求参数

```yaml
sex: "0"

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Sn|header|string| 是 |none|
|body|body|object| 否 |none|
|» sex|body|string| 是 |0为男，1为女 字符串类型|

> 返回示例

> 成功

```json
{
  "code": 0,
  "data": [
    {
      "nickname": "动画",
      "path": "/static/man/anime.jpg",
      "styleid": "663a0bc2af74e609409eac8b"
    },
    {
      "nickname": "皮克斯",
      "path": "/static/man/picas.jpg",
      "styleid": "663a0c01af74e609409eac8c"
    },
    {
      "nickname": "插画",
      "path": "/static/man/illustration.jpg",
      "styleid": "663a0c78af74e609409eac8d"
    },
    {
      "nickname": "油画",
      "path": "/static/man/oilPrinting.jpg",
      "styleid": "663a1039ffd57e84cad2a714"
    },
    {
      "nickname": "写实卡通",
      "path": "/static/man/relCartoon.jpg",
      "styleid": "663a10a6a6060cc90d600cff"
    },
    {
      "nickname": "像素风",
      "path": "/static/man/pixelPrinting.jpg",
      "styleid": "665432eff98df45444d0e8a6"
    },
    {
      "nickname": "古风",
      "path": "/static/man/ancient.jpg",
      "styleid": "6655485f3c71bdd96969d827"
    },
    {
      "nickname": "简笔画",
      "path": "/static/man/simpleLine.jpg",
      "styleid": "665548f33c71bdd96969d828"
    },
    {
      "nickname": "Q版",
      "path": "/static/man/QStyle.jpg",
      "styleid": "665549233c71bdd96969d829"
    },
    {
      "nickname": "水墨画",
      "path": "/static/man/waterColor.jpg",
      "styleid": "665549543c71bdd96969d82a"
    }
  ],
  "msg": "ok"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|[object]|true|none||none|
|»» name|string|true|none||none|
|»» path|string|true|none||none|
|»» styleid|string|true|none||none|
|» msg|string|true|none||none|

## POST 生成图片

POST /generate

> Body 请求参数

```yaml
img: string
style: 0
background: string
raw_img_url: /uploads/2024/06/12/fad4557417764db9a56e9d597b9c821ademo.jpg

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Sn|header|string| 是 |none|
|body|body|object| 否 |none|
|» img|body|string(binary)| 是 |none|
|» style|body|integer| 是 |none|
|» background|body|string| 是 |none|
|» raw_img_url|body|string| 是 |none|

> 返回示例

> 成功

```json
{
  "code": 0,
  "data": {
    "id": "6669473d2d682f8252ea1809",
    "processed_url": "/productions/2024/06/12/e5ae7c0508c442508e45439a3c8139f0demo.jpg",
    "raw_url": "/uploads/2024/06/12/fad4557417764db9a56e9d597b9c821ademo.jpg"
  },
  "msg": "ok"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» id|string|true|none||none|
|» msg|string|true|none||none|
|» data|object|true|none||none|
|»» id|string|true|none||none|
|»» processed_url|string|true|none||none|
|»» raw_url|string|true|none||none|

## POST 保存最终结果

POST /save

> Body 请求参数

```yaml
id: 66249deef250813bdfcff045

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Sn|header|string| 是 |none|
|body|body|object| 否 |none|
|» id|body|string| 是 |none|

> 返回示例

> 成功

```json
{
  "code": 0,
  "data": null,
  "msg": "ok"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|null|true|none||none|
|» msg|string|true|none||none|

## GET 获取静态资源(风格样例图)

GET /static/{path}

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|path|path|string| 是 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

## DELETE 删除图片

DELETE /picture

> Body 请求参数

```yaml
id: 66249deef250813bdfcff045

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» id|body|string| 是 |ID 编号|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

## GET 获取图片资源

GET /minio/{url}

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|url|path|string| 是 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

## POST 获取性别

POST /sex

> Body 请求参数

```yaml
img: file://C:\Users\tianeo\Downloads\4abe5b4e79be4d4ca9b79838034e8471image.png

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Sn|header|string| 是 |none|
|body|body|object| 否 |none|
|» img|body|string(binary)| 是 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

# 非客户端

## POST 添加风格

POST /style

> Body 请求参数

```yaml
name: picas
payload: "{'override_settings': {'sd_model_checkpoint':
  'disneyPixarCartoon_v10'}, 'prompt': 'teenger,(best quality:1.2),cute,looking
  at viewer,masterpiece,delicate face,full of youthful energy,professional,vivid
  colors,bright,live and beautiful eyes', 'negative_prompt': 'NSFW, (worst
  quality:2), (low quality:2), (normal quality:2), lowres, normal
  quality,blurry, ((monochrome)), ((grayscale)),skin spots, acnes, skin
  blemishes, age spot, (ugly:1.331), (duplicate:1.331),(morbid:1.21),
  (mutilated:1.21), (tranny: 1.331), mutated hands,(poorly drawn hands: 1.5),
  (bad anatomy: 1.21), (bad proportions:1.331), extra limbs, (disfigured:1.331),
  (missingarms:1.331), (extra legs: 1.331), (fused fingers: 1.61051), (too many
  fingers: 1.61051), (easynegative:1.2), (unclear eyes: 1.331),(strange
  eyes:1.3),bad hands, missing fingers, extra digit, (((extraarms and legs)))',
  'steps': 35, 'sampler_name': 'Euler a', 'width': 480, 'height': 640,
  'batch_size': 1, 'n_iter': 1, 'seed': -1, 'cfg_scale': 8.5,
  'denoising_strength': 0.35, 'CLIP_stop_at_last_layers': 2, 'init_images': [],
  'restore_faces': False}"
path: /static/picas.jpg

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» name|body|string| 是 |none|
|» payload|body|string| 是 |none|
|» path|body|string| 是 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

# 数据模型

