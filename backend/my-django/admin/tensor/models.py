import tensorflow as tf
from tensorflow import keras
import numpy as np
from matplotlib import pyplot as plt

from admin.common.models import ValueObject

class TensorFunction(object):
    def __init__(self):
        self.vo = ValueObject()
        self.vo.context = 'admin/tensor/data/'

    def hook(self):
        menu = 'exec_by_random_data'
        if menu == 'tf.function':
            pass
            # result = self.tf_function()
        elif menu == 'tf_sum':
            result = self.tf_sum()
        elif menu == 'tf_add':
            result = self.tf_add().summary()
        elif menu == 'create_tf_empty_model':
            self.create_tf_empty_model()
        elif menu == 'exec_by_random_data':
            self.exec_by_random_data()
        else:
            print('해당 사항 없음')
        # print(f'결과 값:{result}')

    def create_tf_empty_model(self):
        '''
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=[150, 150]), # Flatten 은 처음 입력층 으로 , 평평한 층을 먼저 깐다고 생각하면 된다.
            keras.layers.Dropout(rate=0.2),
            keras.layers.Dense(units=1, activation='relu'), # units은 뉴런의 개수를 의미.
            keras.layers.Dropout(rate=0.2),
            keras.layers.Dense(1, activation='softmax') # 1은 신경망의 개수
        ])
        '''
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(units=1, activation='relu', input_dim=1))
        model.add(keras.layers.Dropout(rate=0.2))
        model.add(keras.layers.Dense(units=1, activation='softmax'))
        model.compile(loss='mse', optimizer='sgd')
        model.save(f'{self.vo.context}simple_model1.h5')


    '''
            model = Sequential()    # sequntial 모델 생성 할당 첫번째 층을  
            model.add(Dense(32, input_shape=(16, ))) # 첫번째 층을 dense 32 크기 out 
            model.add(Dense(32))
            Arguments:
            units: 현재 dense 를 통해서 만들 hidden layer 의 Node 의 수
            첫번째 인자 : 출력 뉴런의 수를 설정합니다.
            input_dim : 입력 뉴런의 수를 설정합니다.
            init : 가중치 초기화 방법 설정합니다.
            uniform : 균일 분포
            normal : 가우시안 분포
            activation : 활성화 함수 설정합니다.
            linear : 디폴트 값, 입력뉴런과 가중치로 계산된 결과값이 그대로 출력으로 나옵니다.
            relu : rectifier 함수, 은익층에 주로 쓰입니다.
            sigmoid : 시그모이드 함수, 이진 분류 문제에서 출력층에 주로 쓰입니다.
            softmax : 소프트맥스 함수, 다중 클래스 분류 문제에서 출력층에 주로 쓰입니다.
            다중클래스 분류문제에서는 클래스 수만큼 출력 뉴런이 필요합니다. 
            만약 세가지 종류로 분류한다면, 아래 코드처럼 출력 뉴런이 3개이고, 
            입력 뉴런과 가중치를 계산한 값을 각 클래스의 확률 개념으로 표현할 수 있는 
            활성화 함수인 softmax를 사용합니다.

            https://talkingaboutme.tistory.com/entry/DL-%ED%95%B4%EB%B3%B4%EB%A9%B4%EC%84%9C-%EB%B0%B0%EC%9A%B0%EB%8A%94-%EB%94%A5%EB%9F%AC%EB%8B%9D-ANN-%EA%B5%AC%ED%98%84-2
    '''
    def exec_by_random_data(self):
        model = keras.models.load_model(f'{self.vo.context}simple_model1.h5')
        (x, y) = self.make_rendom_data()
        x_train, y_train = x[:150], y[:150]
        x_test, y_test = x[:150], y[:150]
        history = model.fit(x_train, y_train, epochs=30, validation_split=0.3)
        epochs = np.arange(1, 30 + 1)
        plt.plot(epochs, history.history['loss'], label='Training Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.savefig(f'{self.vo.context}simple_model.png')



    def make_rendom_data(self):
        x = np.random.uniform(low=-2, high=2, size=200)
        y =[]
        for t in x:
            r = np.random.normal(loc=0.0, scale=(0.5 + t * t/3), size=None)
            y.append(r)
        return x, 1.726*x - 0.84 + np.array(y)


    def create_model(self) -> object:
        input = tf.keras.Input(shape=(1,))
        output = tf.keras.layers.Dense(1)(input)
        model = tf.keras.Model(input, output)
        return model



    def tf_add(self):
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        z = tf.add(x, y)
        # z = tf.subtract(x, y)
        # z = tf.multiply(x, y)
        # z = tf.divide(x, y)
        return z


    @tf.function
    def tf_sum(self):
        a = tf.constant(1, tf.int32)
        b = tf.constant(2, tf.int32)
        c = tf.constant(3, tf.int32)
        z = a + b + c
        print(f'@tf.function 사용하기: {z}')
        # for i in range(1, 10):
        #     result = tf.multiply(dan, i)
        #     print(f'결과값: {result}')
        # @tf.function 사용하기: Tensor("add_1:0", shape=(), dtype=int32)
        return z


    def tf_function(self):
        mnist = tf.keras.datasets.mnist
        (X_train, y_train), (X_test, y_test) = mnist.load_data()
        X_train, X_test = X_train / 255.0, X_test / 255.0
        X_train = X_train[..., tf.newaxis] # 차원 추가
        X_test = X_test[..., tf.newaxis]
        train_ds = tf.data.Dataset.from_tensor_slices(
            (X_train, y_train)
        ).shuffle(10000).batch(32)
        test_ds = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(32)
        # batch 쪼개서 배열시킨다,batch 는 한번에 32 이하까지만 쪼개 배열시키는 것이 좋다
        print(f'train_ds : {type(train_ds)}')
        '''
        train_ds : <class 'tensorflow.python.data.ops.dataset_ops.BatchDataset'>
        '''
        # print(list(train_ds.as_numpy_iterator())) 이미지는 출력이 안된다.



class FashionClassification(object):
    def __init__(self):
        self.vo = ValueObject()
        self.vo.context = 'admin/tensor/data/'
        self.class_name = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                           'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    def fashion(self):
        fashion_mnist = keras.datasets.fashion_mnist
        (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
        # self.peek_datas(train_images, test_images, test_labels)
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=[28, 28]),
            keras.layers.Dense(128, activation="relu"),  # neron count 128
            keras.layers.Dense(10, activation="softmax")  # 출력층 활성화함수는 softmax
        ])
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(train_images, train_labels, epochs=5)
        # self.test_and_save_images(model, test_images, test_labels)
        model.save(f'{self.vo.context}fashion_classification.h5')


    def test_and_save_images(self,model, test_images, test_labels):
        test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)  # verbose 는 학습하는 내부상황 보기 중 2번선택
        predictions = model.predict(test_images)
        i = 5
        print(f'모델이 예측한 값 {np.argmax(predictions[i])}')
        print(f'정답: {test_labels[i]}')
        print(f'테스트 정확도: {test_acc}')
        plt.figure(figsize=(6, 3))
        plt.subplot(1, 2, 1)
        test_image, test_predictions, test_label = test_images[i], predictions[i], test_labels[i]
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(test_image, cmap=plt.cm.binary)
        test_pred = np.argmax(test_predictions)

        if test_pred == test_label:
            color = 'blue'
        else:
            color = 'red'
        plt.xlabel('{} : {} %'.format(self.class_name[test_pred],
                                      100 * np.max(test_predictions),
                                      self.class_name[test_label], color))
        plt.subplot(1, 2, 2)
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        this_plot = plt.bar(range(10), test_pred, color='#777777')
        plt.ylim([0, 1])
        test_pred = np.argmax(test_predictions)
        this_plot[test_pred].set_color('red')
        this_plot[test_label].set_color('blue')
        plt.savefig(f'{self.vo.context}fashion_answer2.png')

    def peek_datas(self, train_images, test_images, train_labels):
        print(test_images.shape)
        print(train_images.dtype)
        print(f'훈련 행: {train_images.shape[0]} 열: {train_images.shape[1]}')
        print(f'테스트 행: {test_images.shape[0]} 열: {test_images.shape[1]}')
        plt.figure()
        plt.imshow(train_images[3])
        plt.colorbar()
        plt.grid(False)
        plt.savefig(f'{self.vo.context}fashion_random.png')
        plt.figure(figsize=(10,10))
        for i in range(25):
            plt.subplot(5,5,i+1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(train_images[i], cmap=plt.cm.binary)
            plt.xlabel(self.class_name[train_labels[i]])
        plt.savefig(f'{self.vo.context}fashion_subplot.png')


class Perceptron(object):

    def __init__(self, eta=0.01, n_iter=56, random_state=1):
        '''
        eta :  float 학습률 (0.0과 1.0 사이)
        n_iter : int 훈련 데이터 셋 반복 횟수
        random_state : int 가중치 무작위 초기화를 위한 난수 생성기
        '''
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state


    def fit(self, X,  y) -> object: # 훈련데이터 학습
        '''
        w_ : 1d-array : 학습된 가중치
        errors_ : list 에포크마다 누적된 분류 오류
        '''
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1+X.shape[1])
        self.errors_ = []

        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X,y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def predict(self, X):  # 단위 계단함수를 사용하여 클래스 레이블 반환
        return np.where(self.net_input(X) >= self.w_[0])

    def net_input(self, X):  # 최종 입력 계산
        return np.dot(X, self.w_[1:]) + self.w_[0]


class AdalineGD(object):  # 적응형 선형 뉴런 분류기

    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state


    def fit(self, X, y): # fit은 matrix(DF) 를 만든다.
        # X : {array-like}, shape = [n_samples, n_features]
        #           n_samples 개의 샘플과 n_features 개의 특성으로 이루어진 훈련 데이터

        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1 + X.shape[1])
        self.cost_ = []  # 에포크마다 누적된 비용 함수의 제곱합

        for i in range(self.n_iter):
            net_input = self.net_input(X)
            # Please note that the "activation" method has no effect
            # in the code since it is simply an identity function. We
            # could write `output = self.net_input(X)` directly instead.
            # The purpose of the activation is more conceptual, i.e.,
            # in the case of logistic regression (as we will see later),
            # we could change it to
            # a sigmoid function to implement a logistic regression classifier.
            output = self.activation(net_input)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors ** 2).sum() / 2.0 # errors 가중치?
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, X):
        return X

    def predict(self, X):  # 단위 계단 함수를 사용하여 클래스 레이블을 반환
        return np.where(self.activation(self.net_input(X)) >= 0.0, 1, -1)



class Calculator(object):

    def __init__(self):
        print(f'Tensorflow Version: {tf.__version__}')

    def process(self):
        self.pius(1,6)
        print('*'*100)
        self.mean()

    def pius(self, a, b):
        print(tf.constant(a) + tf.constant(b))

    def mean(self):
        x_array = np.arange(18).reshape(3,2,3)
        # reshape((3 행, 2열 , 3)
        x2 = tf.reshape(x_array, shape=(-1,6)) # shape 으로 다시 변환 -1은 그대로 란 뜻
        # 각 열의 합을 계산
        xsum = tf.reduce_sum(x2, axis=0)
        # 각 열의 평균을 계산
        xmean = tf.reduce_mean(x2, axis=0)

        print(f'입력 크기: {x_array.shape}\n')
        print(f'크기가 변경된 입력 크기: {x2.numpy()}\n')
        print(f'열의 합: {xsum.numpy()}\n')
        print(f'열의 평균: {xmean.numpy()}\n')




