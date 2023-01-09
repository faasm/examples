#include <faasm/core.h>
#include <faasm/faasm.h>
#include <unistd.h>
#include <stdio.h>
#include <string>


bool doChainedCall(const std::string& name, std::string& cmdLine)
{
    unsigned int callId =
      faasmChainNamed(name.c_str(),
                      reinterpret_cast<const uint8_t*>(cmdLine.c_str()),
                      cmdLine.size());

    unsigned int result = faasmAwaitCall(callId);

    return result == 0;
}

int main(int argc, char** argv)
{
    const std::string lammpsFunc = "main";

    // Run LAMMPS twice. Note that `faasmChainNamed` propagates the command
    // line passed to the message
    bool success = true;
    std::string tmpCmdLine = "foo bar";
    success &= doChainedCall(lammpsFunc, tmpCmdLine);
    printf("\n---------------------------------------------------------------\n");
    printf("----------- LAMMPS chaining sleeping between runs ... -----------\n");
    printf("---------------------------------------------------------------\n\n");
    sleep(5);
    // TODO - check for migration oportunities here
    success &= doChainedCall(lammpsFunc, tmpCmdLine);
    return success != true;
}
