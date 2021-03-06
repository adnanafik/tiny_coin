# TinyCoin
Tiny coin in Python is an enhanced version which originally was inspired by Gerald Nash sample code at https://gist.github.com/aunyks/47d157f8bc7d1829a729c2a6a919c173

## Usage

### To run nodes on multiple ports use the following (default is 127.0.0.1:5000)

python app.py --host 127.0.0.1 --port 5001 --debug

python app.py --host 127.0.0.1 --port 5002 --debug

### To add peer to an existing node e.g. 127.0.0.0:5000 use the following 

http://127.0.0.1:5000/peer?node_url=http://127.0.0.1:5001

### To mine a Tinycoin on node running at 127.0.0.1:5000 use the following

http://127.0.0.1:5000/mine

#### Following is a typical mined Tinycoin block!

```json
{
    "target_hash": "fa2109d2e397f8d57799f2c364f3ef3d3bdfbc309457b9630ac14d427150f659",
    "hash": "4038a907f335dd008418664d90c31097d54637544f27fa7172baa5709ee6b634",
    "index": 1,
    "timestamp": "2018-04-11 17:07:58.352593",
    "nonce": "0",
    "data": {
        "proof-of-work": "3d49375dff2968b0d33d05b5e679dd34a87045ecef5c0e0159933ff88ea97bca",
        "transactions": [
            {
                "from": "network",
                "to": "15r2C6Ft5E8fpZkcXECVo2KwT6dRHfzBae",
                "amount": 1
            },
            {
                "signature": "9373ba8e8bb38953470b1e950a828207cd0396bfa8fcdf5b8d90bb0fd87809b4b73be15818c8ab882d3dbd9b3c309ba2c12cb85e2d1dc4990094501b08100723",
                "public key": "b060cc625595ccf4aaad79dfd59bbbf1f6bc04c8f8440427bcaeefd0539e2de888784bfb8b1c01cedaa70971a4ca32bafb4ad32e1f8f8be834536e452ce32162"
            }
        ]
    },
    "previous_hash": "288c6451191f17e767ea14d6b00da1c1be209c2732f964b995621d010bd8445e"
}
```
### To get all the Tinycoins of a given node use the following

http://127.0.0.1:5000/blocks

#### A typical response from the node that has multiple Tinycoins mined!

```json
[
    {
        "target_hash": "fa2109d2e397f8d57799f2c364f3ef3d3bdfbc309457b9630ac14d427150f659",
        "hash": "288c6451191f17e767ea14d6b00da1c1be209c2732f964b995621d010bd8445e",
        "index": 0,
        "timestamp": "2018-04-11 17:06:47.099930",
        "nonce": "0",
        "data": {
            "proof-of-work": null,
            "transactions": null
        },
        "previous_hash": "0"
    },
    {
        "target_hash": "fa2109d2e397f8d57799f2c364f3ef3d3bdfbc309457b9630ac14d427150f659",
        "hash": "4038a907f335dd008418664d90c31097d54637544f27fa7172baa5709ee6b634",
        "index": 1,
        "timestamp": "2018-04-11 17:07:58.352593",
        "nonce": "0",
        "data": {
            "proof-of-work": "3d49375dff2968b0d33d05b5e679dd34a87045ecef5c0e0159933ff88ea97bca",
            "transactions": [
                {
                    "from": "network",
                    "to": "15r2C6Ft5E8fpZkcXECVo2KwT6dRHfzBae",
                    "amount": 1
                },
                {
                    "signature": "9373ba8e8bb38953470b1e950a828207cd0396bfa8fcdf5b8d90bb0fd87809b4b73be15818c8ab882d3dbd9b3c309ba2c12cb85e2d1dc4990094501b08100723",
                    "public key": "b060cc625595ccf4aaad79dfd59bbbf1f6bc04c8f8440427bcaeefd0539e2de888784bfb8b1c01cedaa70971a4ca32bafb4ad32e1f8f8be834536e452ce32162"
                }
            ]
        },
        "previous_hash": "288c6451191f17e767ea14d6b00da1c1be209c2732f964b995621d010bd8445e"
    },
    {
        "target_hash": "fa2109d2e397f8d57799f2c364f3ef3d3bdfbc309457b9630ac14d427150f659",
        "hash": "759d7e806725d46bf3240f65e193b9927127199702e9fb3b973353a8b1ea301c",
        "index": 2,
        "timestamp": "2018-04-11 17:16:30.601984",
        "nonce": "0",
        "data": {
            "proof-of-work": "b11fd9998640709bcb7718db0d7ebd2bf9ee31ffd51b39fc4743c60a90fbf215",
            "transactions": [
                {
                    "from": "network",
                    "to": "15r2C6Ft5E8fpZkcXECVo2KwT6dRHfzBae",
                    "amount": 1
                },
                {
                    "signature": "94ac5e530b2c964c787cc3b49deee5f564f84206be9c61821704043abf79f17301a10452fc30ae67cd465eaca8818e74f5e0d65132b76e9f17d5bb7e61fda08b",
                    "public key": "b060cc625595ccf4aaad79dfd59bbbf1f6bc04c8f8440427bcaeefd0539e2de888784bfb8b1c01cedaa70971a4ca32bafb4ad32e1f8f8be834536e452ce32162"
                }
            ]
        },
        "previous_hash": "4038a907f335dd008418664d90c31097d54637544f27fa7172baa5709ee6b634"
    }
]
```

