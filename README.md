# PackFrame Modpacks

PackFrame 整合包索引仓库。

## 目录

```text
packs/<id>.json     每个整合包一个文件
index.json          GitHub Actions 自动生成，供 App 读取
scripts/build-index.py
.github/workflows/build-index.yml
```

## 提交新整合包

1. 在 `packs/` 下新增 `<id>.json`
2. 提交 Pull Request
3. 合并到 `main` 后，GitHub Action 自动重建 `index.json`
4. App 刷新整合包列表即可看到

每个文件只放一个整合包，多个 PR 同时提交不同文件时不会冲突。

## pack 文件格式

```json
{
  "id": "baseuiandbeauty",
  "name": "UI+美化 [1.7]",
  "summary": "UI+美化 [1.7] 整合包",
  "repo": "ZXUW/BaseUIandBeauty-RimworldPack",
  "ref": "main",
  "manifest": "pack.json",
  "file": "https://raw.githubusercontent.com/ZXUW/BaseUIandBeauty-RimworldPack/main/pack.json",
  "modCount": 83
}
```

- `repo`、`ref`、`manifest` 用于下载整合包仓库。
- `file` 是 App 直接读取的 `pack.json` 地址。
- `modCount` 只用于列表显示。

## 客户端地址

```text
https://raw.githubusercontent.com/ZXUW/PackFrame-Modpacks/main/index.json
```
## License

- Index scripts: [MIT](LICENSE)
- `index.json`, `packs/` and repository documentation: [CC BY 4.0](LICENSE-DATA)
