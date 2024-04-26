# DOSMaster

Link for dosmaster-pypi package(click the icon)

[![PyPI](https://img.shields.io/pypi/v/dosmaster.svg)](https://pypi.org/project/dosmaster/)

Program Name : dosmaster Program

Made by Youngjun Park (yjpark29@postech.ac.kr)

Inspired by Jaesun Kim(CNMD)

Tested by Changhun Kim(CNMD), Suyun Chae(CNMD)

Edit Date : 24/03/10

Description : DOS Plot Smartly in Terminal Environment


version.1.8.3 이 되면 CNMD 구성원 전체에게 공개

### Release History

ver.1.1 : 재시작 시 loading 속도 향상 (by Jaesun Kim)

ver.1.2 : 최종 data 파일 저장 기능 추가

ver.1.3 : 버그 수정

ver.1.4.2 : PyPI에 올릴 수 있도록 수정

ver 1.7.13 : Packaging 진행, DOS_Sum, Average_DOS, Axis_Optimization 추가 및 각종 성능 향상

ver 1.8.1 : Label 버그 수정, 각종 버그 수정, Setting 저장 및 불러오기 기능 구현, DOS plot 저장 및 불러오기 기능 구현, shift_x_axis 구현, 연속된 숫자 입력 기능 확장, legend display 여부 선택 가능

ver 1.8.3 : ISPIN = 1 calculation 지원 및 각종 버그 수정

ver 1.8.4 : Lisence 수정

ver 1.8.5 : f orbital error 수정


## Features
1) Add Atom DOS : 원하는 atom의 DOS를 추가합니다.
2) DOS Projection : 특정 DOS를 원하는 orbital로 projection 시킵니다.
3) Sum DOS : 특정 DOS들의 기여분을 합칩니다.
4) Average DOS : 특정 DOS들의 기여분을 평균화합니다.
5) Remove DOS : 특정 DOS를 지웁니다.
6) Plot only Positive/Negative part : DOS plot의 양/음수 부분만 plot합니다.
7) Edit Graph Style : 원하는 graph style로 바꿉니다.
8) Axis Optimization : 현재의 ylim을 현재의 DOS에 맞게 최적화시킵니다.
9) Import global custom setting (in package) : package 폴더 내의 나만의 graph setting을 불러옵니다.
10) Save global custom setting (in package) : package 폴더 내에 나만의 graph setting을 저장합니다.
11) Import DOSMaster plot from current directory : 현재 위치에 저장된 DOSMaster plot을 불러옵니다.
12) Save DOSMaster plot in current directory : 현재 위치에 지금까지 작업한 DOSMaster plot을 저장합니다.

## Package Download

    $ pip install dosmaster


## Source Code Download

   1) 서버의 ssh-key를 복사 : 다음의 명령어를 git clone할 서버에서 입력하면 나옴.


         $ cat ~/.ssh/id_rsa.pub
   3) 개인 github 계정의 - Settings - SSH keys and GPG keys - New SSH key 클릭
   4) 복사한 ssh-key를 붙여넣고 key를 등록
   5) 서버에서 다음 명령어를 입력하여, 소스코드 다운로드

         $ git clone git@github.com:pyj6767/DOSMaster.git

### Requirements

    $ pip install matplotlib
    $ pip install numpy
    $ pip install pandas
    $ pip install ase
    $ pip install colorama


### Preparation

    $ chmod 774 dosmaster

## Run dosmaster

    $ cd [DOS 계산한 폴더]
    $ dosmaster


## License
DOSMaster is made available under the MIT License.
