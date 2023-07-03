import logging
import traceback
import tempfile
import os
import base64



import gnupg

logging.basicConfig()
logging.root.setLevel(logging.INFO)

# This class is just to quickly play around with the python portion of this to see if it works
def main():
    logging.info(f"Attempting to import key")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:

            b64Key = os.environ["PRIVATE_KEY"]

            base64_bytes = b64Key.encode("ascii")
            sample_string_bytes = base64.b64decode(base64_bytes)
            key_data = sample_string_bytes.decode("ascii")
            #logging.info("DECODED STRING ===== "+key_data)

            gpg = gnupg.GPG(gnupghome=str(tmpdir), verbose=True)
            #logging.info(f"KEY ==== {key_data})")
            import_result = gpg.import_keys(key_data, extra_args=["--yes"])
            logging.info(f"Import Result = {import_result}")
            logging.info(f"--- Print Import Results ---")
            for k in import_result.results:
                print(k)
            logging.info(f"--- Done Importing ---")
            #stream = open(myblob, 'rb')
            f = open("/Users/robin/Downloads/noncrypt.txt.gpg", 'rb')
            #f = open("/Users/robin/Downloads/text.txt")
            #logging.info("File === "+str(f.read()))
            content = f.read()
            logging.info("File === "+str(content))
            decrypted_data = gpg.decrypt(content, always_trust=True)
            #decrypted_data = gpg.decrypt_file(f, always_trust=True)
            #blobout.set(str(decrypted_data))
            logging.info(f"Decrypt Status is = {decrypted_data}")
            logging.info(f"Decrypted data === {str(decrypted_data)} did it work?")
            logging.info(f"----- Done")
    except Exception as e:
        logging.info("An error occured either when importing or decrypting")
        logging.error(traceback.format_exc())

main()