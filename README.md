# PackFrame Modpacks

PackFrame 的整合包索引仓库。

## 目录

```text
index.json          整合包列表
packs/<id>.json     单个整合包详情
images/             封面和截图
```

## 添加整合包

1. 在 `packs/<id>.json` 写入整合包详情。
2. 在 `index.json` 的 `packs` 数组中加入同 `id` 的条目。
3. 把封面放到 `images/`，路径相对于仓库根目录。
4. 提交并推送后，在 PackFrame 中填写：

```text
https://raw.githubusercontent.com/<user>/<repo>/main/index.json
```

## index.json

```json
{
  "schemaVersion": 1,
  "packs": [
    {
      "id": "example",
      "name": "示例整合包",
      "summary": "一句话介绍",
      "image": "images/example.png",
      "modCount": 3
    }
  ]
}
```

`file` 可省略，默认读取 `packs/<id>.json`。如要使用其他路径，可写 `"file": "packs/example.json"`。

## packs/<id>.json

```json
{
  "name": "示例整合包",
  "author": "作者",
  "description": "整合包介绍",
  "gameVersion": "1.6",
  "workshopCollectionId": "1234567890",
  "mods": [
    {
      "source": "workshop",
      "name": "工坊模组",
      "workshopId": "123456789",
      "packageId": "author.mod"
    },
    {
      "source": "github",
      "name": "GitHub 模组",
      "downloadUrl": "https://github.com/user/repo/releases/download/v1/Mod.zip"
    },
    {
      "source": "local",
      "name": "本地模组",
      "path": "D:\\Mods\\MyMod",
      "packageId": "author.local"
    }
  ],
  "packageIds": [
    "author.mod",
    "author.local"
  ]
}
```

### 字段说明

- `workshopCollectionId`：创意工坊合集 ID；安装时会展开合集中的物品并订阅。
- `workshopUrl`：也可直接写创意工坊合集或模组链接。
- `mods[].source`：`workshop`、`github`、`local`、`official`。
- `mods[].workshopId`：工坊物品 ID，可写纯数字或工坊链接。
- `mods[].packageId`：RimWorld 的 PackageId。**工坊模组建议填写**，否则要等 Steam 下载完成后才能确定并自动启用。
- `mods[].downloadUrl`：GitHub ZIP 直链，最稳妥。
- `mods[].repo`：GitHub 仓库 `owner/repo`；可选 `asset`（release 文件名）和 `tag`。未指定 asset 时优先使用 latest release 的 zip，没有 release 时使用默认分支 ZIP。
- `mods[].path`：本地模组绝对路径。远程仓库一般不要填写，改用 `packageId` 让客户端使用已安装的本地模组。
- `packageIds`：整体启用顺序的兜底列表。安装后 PackFrame 会按这个顺序写入新实例的 `ModsConfig.xml`。

## 安装行为

PackFrame 点击“整合包”后读取 `index.json`，选择整合包并安装时会：

1. 下载 GitHub ZIP 并解压到根目录 `mods/`。
2. 复制本地模组到 `mods/`（如果提供路径且不存在则使用已安装的同 PackageId 模组）。
3. 展开工坊合集并通过 Steam 订阅其中的物品。
4. 自动新建实例、写入启用列表，并在当前实例栏选中。

SteamCMD 下载暂未支持。
