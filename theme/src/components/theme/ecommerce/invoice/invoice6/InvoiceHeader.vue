<template>
    <div>
        <div class="row">
            <div class="col-sm-6">
                <div class="d-flex">
                    <div class="media-left"><img class="media-object img-60 for-light"
                            src="@/assets/images/other-images/logo-login.png" alt="">

                    </div>
                    <div class="flex-grow-1 m-l-20 text-right">
                        <h4 class="media-heading">MOfi </h4>
                        <p>hello@Mofi.in<br><span>289-335-6503</span></p>
                    </div>
                </div>

            </div>
            <div class="col-sm-6">
                <div class="text-md-end text-xs-center">
                    <h3>Invoice #<span class="counter">
                            <number class="bold counter" ref="number1" :from="0" :to="1069" :duration="5" :delay="0"
                                easing="Power1.easeOut" />
                        </span></h3>
                    <p>Issued: May<span> 27, 2024</span><br> Payment Due: June <span>27, 2024</span></p>
                </div>

            </div>
        </div>
    </div>
</template>