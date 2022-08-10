from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=64, verbose_name='글 제목')
    contents = models.TextField(verbose_name='글 내용')
    writer = models.CharField(max_length=32,verbose_name='작성자')
    sentence = models.CharField(max_length=64, verbose_name='문장', default="")
    write_dttm = models.DateTimeField(auto_now_add=True, verbose_name='글 작성일')

    board_name = models.CharField(max_length=32, default='Public', verbose_name='게시판 종류')
    update_dttm = models.DateTimeField(auto_now=True, verbose_name='최종 수정일')
    hits = models.PositiveIntegerField(default=0, verbose_name='조회수')

    image = models.ImageField(blank=True, null=True, verbose_name='썸네일 이미지', upload_to = "Images/") 
    file = models.FileField(blank=True, null=True, verbose_name='첨부 파일', upload_to = "Files")

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'board'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'