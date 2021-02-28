# Teeth Object Detection

> Promedius.inc 회사에서 ML team 인턴으로 참여중일 때, Panorama film에서 치아를 찾아내고 각 치아에 대해 numbering을 진행하는 Challenge를 참여하면서 작성한 postprocessing에 대해서 정리를 해보려 한다.
>
> Reference : A deep learning approach to automatic teeth detection and numbering based on object detection in dental periapical flms(link : https://www.nature.com/articles/s41598-019-40414-y)
>
> Challenge Information : http://aifactory.space/task/detail.do?taskId=T001727 Task : 1(치과 파노라마 사진(X-ray)의 치아 번호를 식별하라 주최 : 삼성서울병원 아주대학교병원)

## Introduction

> 치과 파노라마 사진(X-ray)의 치아 번호를 식별하는 Challenge를 팀으로 참가하여 진행하였는데, 각자 진행할 내용에 대해서 생각을 하면서 나는 model output에 대한 postprocessing을 전담해서 진행해보고 싶었다. 최근 딥러닝의 Object Detection 분야에서 기술이 급격하게 성장하면서 웬만한 object는 기존의 model에서 충분히 찾아낼 것으로 생각하였고, 챌린지의 특성상 하나 차이로 갈리기도 하기 때문에 한 class에 대해서도 실수가 발생하면 점수에 큰 영향을 미칠 것으로 판단하였다.

## Contents

> 해당 code는 모델에 대한 output으로 box에 대한 class, confidence score, coordinate가 나올 때, class에 대한 정보와 confidence score를 input으로 받는다. 
>
> 논문에서는 detection한 class와 confidence score를 바탕으로 기존의 치아 template과 비교를 하고 comparison score를 계산하여 Comparison score가 높은 방향으로 output을 template과 비교하고, output의 class를 template의 순서로 replace를 진행한다.
>
> 여기서 나는 output이 나오면 그거를 왼쪽 위의 치아부터 순서대로 Python 자료구조의 list로 Class와 Confidence score를 받고 return 값도 리스트로 반환하여 json 파일에 replace를 진행하였다.

## Requirements

> numpy 