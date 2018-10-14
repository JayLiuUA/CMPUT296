function Complex2(real, imag) {
  var obj = Object.create(proto);
  obj.real = real;
  obj.imag = imag;
  return obj;
}
var proto = {
  magnitude: function() {
    return Math.sqrt(this.real ** 2 + this.imag ** 2);
  }
};
