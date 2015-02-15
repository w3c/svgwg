#!/usr/bin/env perl

# Searches for un-numbered issues in a spec and assigns them the next
# available issue number.

sub readfile {
  my $fn = shift;
  local $/;
  open my $fh, $fn;
  my $contents = <$fh>;
  close $fh;
  return $contents;
}

die "usage: $0 SOURCEFILE DATAFILE\n" unless @ARGV == 2;

my $sourcefn = shift @ARGV;
my $datafn = shift @ARGV;
my %data;

die "source file $sourcefn not found\n" unless -f $sourcefn;

if (-f $datafn) {
  open FH, $datafn;
  while (<FH>) {
    chomp;
    my ($filename, $nextid) = split;
    $data{$filename} = $nextid;
  }
  close FH;
}

$data{$sourcefn} = 1 unless defined $data{$sourcefn};

my $datachanged = 0;
my $sourcechanged = 0;

my $source = readfile($sourcefn);
my $newsource = '';
while ($source ne '') {
  if ($source =~ s/^(.*?)(<(p|div)[^>]*)>//s) {
    $newsource .= $1;
    my $tag = $2;
    if ($tag =~ /class="([^"]*)"/ ||
        $tag =~ /class='([^']*)'/) {
      my $class = $1;
      if ($class =~ /\bissue\b/) {
        if ($tag =~ /data-issue="([^"]*)"/ ||
            $tag =~ /data-issue='([^']*)'/) {
          my $n = $1;
          die unless $n =~ /[0-9]+/;
          if ($n >= $data{$sourcefn}) {
            $data{$sourcefn} = $n + 1;
            $datachanged = 1;
          }
        } else {
          my $n = $data{$sourcefn}++;
          $tag .= " data-issue=\"$n\"";
          $datachanged = 1;
          $sourcechanged = 1;
        }
      }
    }
    $newsource .= $tag . '>';
  } else {
    $newsource .= $source;
    $source = '';
  }
}

if ($sourcechanged) {
  open FH, ">$sourcefn";
  print FH $newsource;
  close FH;
}

if ($datachanged) {
  open FH, ">$datafn";
  for my $k (sort keys %data) {
    print FH "$k $data{$k}\n";
  }
  close FH;
}
