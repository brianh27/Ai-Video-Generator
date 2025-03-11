import time
import requests
import json
def transcribe():

    #CODE COPIED FROM SPEECHIFY API
    # Constants
    REVAI_ACCESS_TOKEN = "02p80zIalqAbAX3SReFAiehq00jZ6wJS6l9n0GrqTQXlMUDBP52xYo5_bs2YiH1LmLD83WkWQjlB_dfoH2H_O98_-_iq8"  # Replace with your Rev AI access token
    AUDIO_FILE_PATH = "audio.mp3"  # Replace with the path to your local audio file

    # API URLs
    BASE_URL = "https://api.rev.ai/speechtotext/v1"
    JOB_SUBMISSION_URL = f"{BASE_URL}/jobs"
    JOB_STATUS_URL = f"{BASE_URL}/jobs"
    TRANSCRIPT_URL = f"{BASE_URL}/jobs/{{job_id}}/transcript"
    SUBTITLE_URL = f"{BASE_URL}/jobs/{{job_id}}/captions"


    def submit_audio_file():
        """Submit the local audio file for transcription and return the job ID."""
        headers = {
            "Authorization": f"Bearer {REVAI_ACCESS_TOKEN}",
        }
        files = {
            "media": open(AUDIO_FILE_PATH, "rb"),  # Open the local audio file in binary mode
            "metadata": (None, "Transcription job for local audio.mp3")
        }

        response = requests.post(JOB_SUBMISSION_URL, headers=headers, files=files)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        job_id = response.json()["id"]
        print(f"Job submitted successfully. Job ID: {job_id}")
        return job_id


    def check_job_status(job_id):
        """Check the status of the transcription job."""
        headers = {"Authorization": f"Bearer {REVAI_ACCESS_TOKEN}"}
        response = requests.get(f"{JOB_STATUS_URL}/{job_id}", headers=headers)
        response.raise_for_status()
        return response.json()["status"]


    def download_json_transcript(job_id):
        """Download and save the JSON transcript."""
        headers = {
            "Authorization": f"Bearer {REVAI_ACCESS_TOKEN}",
            "Accept": "application/vnd.rev.transcript.v1.0+json"
        }
        response = requests.get(TRANSCRIPT_URL.format(job_id=job_id), headers=headers)
        response.raise_for_status()
        json_transcript = response.json()
        with open("transcript.json", "w") as json_file:
            json.dump(json_transcript, json_file, indent=2)
        print("JSON transcript saved to 'transcript.json'.")


    def download_srt_file(job_id):
        """Download and save the subtitle file in .srt format."""
        headers = {
            "Authorization": f"Bearer {REVAI_ACCESS_TOKEN}",
            "Accept": "application/x-subrip"
        }
        response = requests.get(SUBTITLE_URL.format(job_id=job_id), headers=headers)
        response.raise_for_status()
        with open("script.srt", "wb") as srt_file:
            srt_file.write(response.content)
        print("Subtitle file saved to 'script.srt'.")


    def main():
        try:
            # Step 1: Submit the audio file
            job_id = submit_audio_file()

            # Step 2: Wait for the transcription to complete
            print("Waiting for transcription to complete...")
            while True:
                status = check_job_status(job_id)
                if status == "transcribed":
                    print("Transcription completed.")
                    break
                elif status == "failed":
                    raise RuntimeError("Transcription failed.")
                time.sleep(1)  # Wait for 10 seconds before polling again

            # Step 3: Retrieve and save the transcripts
            print("Retrieving transcripts...")
            download_json_transcript(job_id)
            download_srt_file(job_id)

        except Exception as e:
            print(f"An error occurred: {e}")


    if __name__ == "__main__":
        main()
transcribe()