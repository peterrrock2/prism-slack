def __init__(self, core, plugin):
    core = core


def postSubmit_Deadline(self, origin, result, jobInfos, pluginInfos, arguments):
    deadline = self.core.getPlugin("Deadline")

    job = jobInfos.get("BatchName") or jobInfos.get("Name")
    if not job:
        print("ERROR: Job name not found, skipping submission.")
        return

    if "_publishToSlack" in job:
        print(
            f"Job {job} is already a publishToSlack job. Skipping post-job submission."
        )
        return

    job_batch = job
    output = jobInfos.get("OutputFilename0")
    output = output.replace("\\", "/")

    job_dependency = deadline.getJobIdFromSubmitResult(result)
    if not job_dependency:
        print("ERROR: Could not extract Job ID from Deadline response.")
        return

    state_data = {
        "rangeType": state.cb_rangeType.currentText(),
        "startFrame": state.l_rangeStart.text(),
        "endFrame": state.l_rangeEnd.text(),
        "convertMedia": state.chb_mediaConversion.isChecked(),
    }
    comment = self.get_slack_comement()
    code = self.deadline_submission.deadline_submission_script(
        output, state_data, comment, type="render", ui="DL"
    )

    deadline.submitPythonJob(
        code=code,
        jobName=job + "_publishToSlack",
        jobPrio=80,
        jobPool=jobInfos.get("Pool"),
        jobSndPool=jobInfos.get("SecondaryPool"),
        jobGroup=jobInfos.get("Group"),
        jobTimeOut=180,
        jobMachineLimit=jobInfos.get("MachineLimit"),
        # jobBatchName = job_batch,
        frames="1",
        suspended=jobInfos.get("InitialStatus") == "Suspended",
        jobDependencies=job_dependency,
        args=arguments,
        state=state,
    )
