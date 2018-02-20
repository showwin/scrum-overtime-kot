# scrum-overtime-kot

KING OF TIME (KOT)のAPIを叩いてスプリント毎のチームの残業時間を集計するツール

## 詳細

スクラムの手法を使って開発しているチーム向けのツールです。
べろしてぃーが〜
残業時間かくにんしないと〜


## インストール

```
$ pip install sokot  # TODO
```

## 使い方

```
$ sokot configure
$ sokot available  # token が有効か確認
$ sokot group add dev_team_1 0003 A0004 0011  # 'dev_team_1' チームを追加して、KOTのメンバーコードでメンバーを追加
$ sokot overtime
|------------|------------|
| Sprint No. | dev_team_1 |
|------------|------------|
| Sprint #1  | 30.1 hour  |
|------------|------------|
| Sprint #2  | 12.1 hour  |
|------------|------------|
| Sprint #3  | 34.7 hour  |
|------------|------------|
| Sprint #4  | 20.4 hour  |
|------------|------------|
| Sprint #5  | 28.0 hour  |
|------------|------------|
```

## TODO

* [ ] API禁止時間帯のメッセージ表示
  * レスポンス: `{'errors': [{'message': '次の時間帯（JST）はAPIへのアクセスが禁止されています [08:30 ～ 10:00, 17:30 ～ 18:30]', 'code': 104}]}`
* [ ] オプションで HTTP Proxy の設定追加
* [ ] 集計方法に `sum` と `per_member` を追加
