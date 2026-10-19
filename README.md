# PackFrame Modpacks

PackFrame 的整合包索引仓库。

## 目录

```text
index.json          整合包索引
```

每个整合包的数据、模组和配置都在各自独立的仓库中。

## index.json

```json
{
  "schemaVersion": 2,
  "packs": [
    {
      "id": "baseuiandbeauty",
      "name": "BaseUIandBeauty",
      "summary": "整合包简介",
      "repo": "ZXUW/BaseUIandBeauty-RimworldPack",
      "ref": "main",
      "manifest": "pack.json",
      "file": "https://raw.githubusercontent.com/ZXUW/BaseUIandBeauty-RimworldPack/main/pack.json",
      "modCount": 83
    }
  ]
}
```

- `repo`、`ref`、`manifest` 用于后续按整合包仓库加载。
- `file` 是当前加载器直接读取的 `pack.json` 地址。
- `modCount` 只用于列表显示。

## 客户端地址

```text
https://raw.githubusercontent.com/ZXUW/PackFrame-Modpacks/main/index.json
```

## 整合包仓库结构

```text
BaseUIandBeauty-RimworldPack/
  pack.json
  config/ModsConfig.xml
  config/Mod_*.xml
  mods/BaseUIandBeautyTweak/
  images/
```
