rmdir /s /q lib.linux-x86_64-3.9
docker build -f .\Buildfile . -t appbuild:latest
docker run --name appbuild -d appbuild
docker cp appbuild:/appbuild/build/lib.linux-x86_64-3.9 .
docker rm --force appbuild
docker image rm appbuild
