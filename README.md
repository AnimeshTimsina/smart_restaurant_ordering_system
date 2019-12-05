# Smart Restaurant Ordering System


#### Resources:

- Django   
- PostgreSQL
- Redis
- Turicreate
- Pandas
- Numpy
- Django-paypal 


### Steps:
- Inside Project directory:

    `pip install -r requirements.txt`

- Run redis server on default port:
    `redis-server`
    If it fails to start
    Linux: `systemctl restart redis-server`
         : `systemctl enable redis-server`
    MacOS: `redis-server /etc/redis.conf`
    Windows `redis-server --service-start`
    
- Create a postgres database named srosdb and import the provided test sql file to this database
  
  `psql -U [USERNAME] [DBNAME] < srosdb.sql`
    

- Inside metamask, create a new server with the same RPC server address as in Ganache
- Import Accounts on Metamask from Ganache using the private keys of the addresses
- Reload the browser

### For QR CODE SCANNER:

- Go to directory 'User Authentication Cross Platform Mobile Application'
- `npm install expo-cli --global`
- `npm install`
- `expo start -c`
- Either run on an emulator or install expo app on your phone and scan the QR code to open the app on your phone
- Add ganache provided id keys on election.json file (Only the accounts with these keys are authorized to vote)
- Open any online QR code generator, embed one of these keys and create a QR code. Also for testing purpose, create another QR code with     any text except the key
- Open the app and scan these QR codes one by one
- Authentication succeeds or fails depending upon the validity of key in the QR code
- You can now vote as soon as the user is authenticated


### Screenshots


![Screen Shot 2019-12-05 at 20 29 53](https://user-images.githubusercontent.com/43087414/70253181-d6921b00-17aa-11ea-90a7-f4d0ab323979.png)
![Screen Shot 2019-12-05 at 20 30 08](https://user-images.githubusercontent.com/43087414/70253182-d6921b00-17aa-11ea-9bfa-1c3e283620c6.png)
![Screen Shot 2019-12-05 at 20 30 20](https://user-images.githubusercontent.com/43087414/70253184-d72ab180-17aa-11ea-922d-1e848cd5fd0b.png)
![Screen Shot 2019-12-05 at 20 30 29](https://user-images.githubusercontent.com/43087414/70253185-d7c34800-17aa-11ea-90a2-39349a28423a.png)
![Screen Shot 2019-12-05 at 20 31 02](https://user-images.githubusercontent.com/43087414/70253187-d8f47500-17aa-11ea-9f3e-c55208bd3d6e.png)
![Screen Shot 2019-12-05 at 20 31 24](https://user-images.githubusercontent.com/43087414/70253188-d8f47500-17aa-11ea-953d-4a8083a1ab14.png)
![Screen Shot 2019-12-05 at 20 31 46](https://user-images.githubusercontent.com/43087414/70253194-dabe3880-17aa-11ea-9b03-d6b71fa6ee56.png)
