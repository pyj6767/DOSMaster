# DOSMaster
Program Name : dosmaster Program

Made by Youngjun Park (yjpark29@postech.ac.kr)

Inspired by Jaesun Kim

Edit Date : 23/10/11

Description : DOS Plot Smartly in Terminal Environment



ver.1.1 : 재시작 시 loading 속도 향상 (by Jaesun Kim)

ver.1.2 : 최종 data 파일 저장 기능 추가

ver.1.3 : 버그 수정

ver.1.4.2 : PyPI에 올릴 수 있도록 수정

ver 1.7.13 : Packaging 진행, DOS_Sum, Average_DOS, Axis_Optimization 추가 및 각종 성능 향상

ver 1.8.1 : Label 버그 수정, 각종 버그 수정, Setting 저장 및 불러오기 기능 구현, DOS plot 저장 및 불러오기 기능 구현, shift_x_axis 구현, 연속된 숫자 입력 기능 확장, legend display 여부 선택 가능


## Features
1) Add Atom DOS
2) DOS Projection
3) Sum DOS
4) Average DOS
5) Remove DOS
6) Plot only Positive/Negative part
7) Edit Graph Style
8) Axis Optimization
9) Import global custom setting (in package)
10) Save global custom setting (in package)
11) Import DOSMaster plot from current directory
12) Save DOSMaster plot in current directory


## Future Update (ver.1.8.2)
13) ISPIN=1 Support (Not Implemented)
14) Subplot


## Package Download

    $ pip install dosmaster


## Source Code Download

   1) 서버의 ssh-key를 복사 : 다음의 명령어를 git clone할 서버에서 입력하면 나옴.


         $ cat ~/.ssh/id_rsa.pub
   3) 개인 github 계정의 - Settings - SSH keys and GPG keys - New SSH key 클릭
   4) 복사한 ssh-key를 붙여넣고 key를 등록
   5) 서버에서 다음 명령어를 입력하여, 소스코드 다운로드

         $ git clone git@github.com:pyj6767/DOSMaster.git

### Source Code Requirements

    $ pip install matplotlib
    $ pip install numpy
    $ pip install pandas
    $ pip install ase
    $ pip install colorama
    $ pip install PyYAML


### Source Code Preparation

    $ chmod 774 dosmaster

## Source Code Run dosmaster

    $ cd [DOS 계산한 폴더]
    $ dosmaster
