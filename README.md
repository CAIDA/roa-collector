# ROA Collector

This program downloads the validated RPKI ROAs from RIPE NCC's validator site and output to compressed JSON files.

## Install

```shell
python3 setup install --user
```

## Usage

There are two subcommands:
- `roa-collector now`: download the most recent ROA lists from the API endpoint at https://rpki-validator.ripe.net/api/export.json. There is no parameters for this subcommand.
- `roa-collector hist`: download historical ROAs from the RIPE's FTP site at "https://ftp.ripe.net/rpki/". There are two parameters to allow narrowing down the search time range to a year or a month:
  - `--year Y`: only download ROAs for `Y` year
  - `--month M`: only download ROAs for `M` month (needs to specify `--year` as well)

**Required parameter**:
- `-d` (`--dir`): specify the directory to which the data should be downloaded to

## Data Storage

The historical data (daily) is downloaded to: 
- `ROOT_DATA_DIR/YEAR/MONTH/DAY/roas.daily.UNIX_TIMESTAMP.json.gz`

The current data (every 5 minutes) is downloaded to: 
- `ROOT_DATA_DIR/YEAR/MONTH/DAY/HOUR/roas.5min.UNIX_TIMESTAMP.json.gz`

## Data Format

The historical data and real-time data share the same JSON format:
```json
{
  "roas": [
    {
      "asn": "AS37674",
      "prefix": "41.191.212.0/22",
      "maxLength": 24,
      "ta": "AfriNIC RPKI Root"
    },
    {
      "asn": "AS37674",
      "prefix": "41.242.144.0/21",
      "maxLength": 24,
      "ta": "AfriNIC RPKI Root"
    },
    ...
  ]
}
```

## Crontab Config

The following cronjobs runs roa-collector per 5-min for 5min-bin data and every 6 hours for daily data:
```
# downloading real-time ROAs
*/5 * * * * /usr/local/bin/roa-collector -d /data/rpki/roas now

# download historical ROAs
0 */6 * * * /usr/local/bin/roa-collector -d /data/rpki/roas hist --current-month
```

## Docker setup

### Build container

Checkout the repository and run the following command to build the image:
```sh
docker build -f Dockerfile -t roa-collector .
```

### Run container

We first need a data direcotry to store downloaded ROA data.

Assuming we have an directory ~data~ created for this purpose, then we can run the following command to download the most recent ROAs:

``` sh
docker run --rm -it -v $PWD/data:/data roa-collector roa-collector -d /data now
```

Note that this command mounts the current directory's ~data~ directory to ~/data~ in the container,
and then specify that directory when running the ~roa-collector~ command. The usage of the command is the same as described above.
