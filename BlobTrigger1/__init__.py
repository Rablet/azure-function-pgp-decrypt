import logging
import traceback
import tempfile
import os
import base64

import azure.functions as func
import gnupg

logging.basicConfig()
logging.root.setLevel(logging.INFO)


def main(myblob: func.InputStream, outputblob: func.Out[str]):
    logging.info(f"Starting decryption of blob {myblob.name} ({myblob.length} bytes)")

    # The key is stored base64 envoded. Convert that to string here
    base64_key = os.environ["PRIVATE_KEY"]
    base64_bytes = base64_key.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    key_data = sample_string_bytes.decode("ascii")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            gpg = gnupg.GPG(gnupghome=str(tmpdir), verbose=True)
            logging.info("Attempting to import key")
            import_result = gpg.import_keys(key_data, extra_args=["--yes"])
            logging.info(f"Import Result = {import_result}")
            logging.info("--- Print Import Results ---")
            for k in import_result.results:
                logging.info(k)
            logging.info("--- Done Importing ---")
            content = myblob.read()
            decrypted_data = gpg.decrypt(content, always_trust=True)
            #logging.info(f"Decrypt Status is = {decrypted_data}")
            logging.info(f"Decrypted data ===> {str(decrypted_data)} <=== did it work?")
            outputblob.set(str(decrypted_data))


    except Exception as e:
        logging.info("An error occured either when importing or decrypting")
        logging.error(traceback.format_exc())
    logging.info(f"Finished processing blob {myblob.name}")