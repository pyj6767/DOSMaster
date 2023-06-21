# DOSMaster
Program Name : dosmaster Program

Made by Youngjun Park (yjpark29@postech.ac.kr)

Inspired by Jaesun Kim

Edit Date : 23/06/21

Description : DOS Plot Smartly

ver.1.1 : 재시작 시 loading 속도 향상 (by Jaesun Kim)

ver.1.2 : 최종 data 파일 저장 기능 추가

ver.1.3 : 버그 수정


## Source Code Download

   1) 서버의 ssh-key를 복사 : 다음의 명령어를 git clone할 서버에서 입력하면 나옴.
   
   
         $ cat ~/.ssh/id_rsa.pub
   3) 개인 github 계정의 - Settings - SSH keys and GPG keys - New SSH key 클릭
   4) 복사한 ssh-key를 붙여넣고 key를 등록
   5) 서버에서 다음 명령어를 입력하여, 소스코드 다운로드
   
         $ git clone git@github.com:pyj6767/DOSMaster.git


## Features
1) Add Atom DOS
2) DOS Projection
3) Remove DOS
4) Edit Graph Style
5) Plot only Positive/Negative part

---------------- (Future Version) -------------------

6) DOS sum (Not Implemented)
7) ISPIN=1 Support (Not Implemented)
8) Find Max Contribution Atom DOS (Not Implemented)
9) Edit Legend Name (Not Implemented)

## Requirements

    $ pip install matplotlib
    $ pip install numpy
    $ pip install pandas
    $ pip install ase


## Installation Preparation

    $ chmod 774 dosmaster

## Run dosmaster

    $ cd [DOS 계산한 폴더]
    $ dosmaster
