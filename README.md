# SendGrid Wrapper

## Description

SendGrid Wrapper is a utility program that makes it easier to send email with SendGrid.

## Getting Started

First, you will need to export your SendGrid API key.

```bash
export SENDGRID_API_KEY=<YOUR_API_KEY>
```

Next, you can choose between using either the CLI or the interactive console.

### CLI

#### Help Menu

```bash
python sendgrid_cli.py --help
```

#### Example

``` bash
python sendgrid_cli.py --sender=anujshah26@gmail.com --recipient=anujshah26@gmail.com --subject=Test --message="Hello World" --categories="cats,dogs,birds" --schedule="02-21-2020 23:50:00"
```

### Interactive Console

```bash
python sendgrid_console.py
```
