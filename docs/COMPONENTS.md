# Components

The following documentation explains how to define the other components like
the IP and DM in the config.

## Image Processors

You are able to connect multiple IPs to one core. The structure in the config
is as follows:

```yaml
image_processors:
  - name: "Example"
    hostname: "localhost"
    port: 3000
  - name: "Bedroom"
    hostname: "192.168.2.26"
    port: 25874
```

`name` is being ignored by the core as it is only present to identify the IP
in the config. It can therefore be left empty.  
`hostname` is either an IP, URL or local domain used to connect to the IP.  
`port` is the port the IP is listening on.

## Device Managers

The definition is the same as the one from the IPs, except that the top level
keyword is `device_managers`. Example:

```yaml
device_managers:
  - name: "Home NAS"
    hostname: "nas.example.com"
    port: 5000
  - name: "Homenet ESP32"
    hostname: "192.168.2.100"
    port: 36487
```

The values have the same effect as the ones from the IP.
