# alugvps-server
Server backend software for managing remote Linux LXC containers

## Libraries/Technologies Used
- Uvicorn
- FastAPI
- LXD
- SQLModel
- PyJWT
- python-dotenv
- aiosmtpd

## Things that must be implemented:
- Implement email-based 2FA
- Cleaner web user interfance (UI/UX)

## Setting up a configuration
You will need a `.env` file to run in the same directory as `alugvps-server.py`. Here are the environment variables to specify in `.env`:

- "secret_key" - Use this command to generate a secret key: openssl rand -hex 32
- "port" - Connection Port
- "acc_limit" - Number of Accounts that can have Containers at a Given Time
- "cpu_limit" - CPU Core Limit for Containers
- "ram_limit" - RAM Limit for Containers
- "disk_limit" - Disk Space Limit for Containers
- "fingerprint_image" - LXC Container Image (See them via `lxc image list`)
- "email" - Email where communications will be sent from
- "email_key" - Email key
- "smtp_host" - SMTP Host
- "smtp_port" - SMTP Port

## Run via Docker
In the root directory of the source code, run this command:

`docker build -t alugvps-server .`

Once it has been built, initialize a Docker container with the following command:

`docker run -it --mount type=bind,src={LXD Socket Directory},dst={LXD Socket Directory} --mount type=bind,src={Host .env File Directory},dst=/usr/local/alugvps-server/.env -p {Listening Port on Host}:{Connection Port in .env File} --name {Name Your Set Up} alugvps-server`

The LXD Socket Directory will vary by system, however for Snap installations, it will be located at `/var/snap/lxd/common/lxd/unix.socket`. Otherwise, it will be at `/var/lib/lxd/unix.socket`. So mount whatever the location is in the specified parameters.